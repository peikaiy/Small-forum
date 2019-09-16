from django.core.cache import cache

# def page_cache(timeout):
#     def wrapper1(view_func):
#         def wrapper2(request):
#             key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
#             response = cache.get(key)
#             print('Get from cache', response)
#             if response is None:
#                 response = view_func(request)
#                 print('Get from view', response)
#                 cache.set(key, response, timeout)
#             return response
#         return wrapper2
#     return wrapper1


# 帖子缓存


from common import rds
from post.models import Post

"""
    获取cache有直接获取
    没有存入 存model
"""


# 页面缓存
def page_cache(timeout):
    def wrapper1(view_func):
        def wrapper2(request):
            key = "PageCache-%s-%s" % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            # print("Get from cache", response)
            if response is None:
                response = view_func(request)
                # print("Get from cache", response)
                # print("set  cache", response)
                cache.set(key, response, timeout)
            return response

        return wrapper2

    return wrapper1


# 阅读计数
def read_count(read_view):
    def wrapper(request):
        post_id = int(request.GET.get("post_id"))
        # 阅读计数 排行名  计数的帖子 增加数值
        rds.zincrby("ReadRank", post_id)
        # print(rds.zrevrange("ReadRank",0, 9,withscores=True) )
        return read_view(request)

    return wrapper


# 取出TOP_N帖子及其计数
def get_top_n(num):
    # 从redis中取出原始数据
    ori_data = rds.zrevrange("ReadRank", 0, num - 1, withscores=True)
    # ori_data = [
    #     (b'36', 1183.0),
    #     (b'3',   233.0),
    #     (b'37',  164.0),
    #     ...
    # ]

    # 数据清洗
    cleaned_rank = [[int(post_id), int(count)] for post_id, count in ori_data]
    # cleaned_rand = [
    #     [36, 1183],
    #     [ 3,  233],
    #     [37,  164],
    # ]

    # 思路一：直接替换
    # for item in cleaned_rank:
    #     item[0] = Post.objects.get(id=item[0])
    # rank_data = cleaned_rank

    # 思路二：批量获取 Post
    post_id_list = [post_id for post_id, _ in cleaned_rank]
    # 批量取出posts
    posts = Post.objects.filter(id__in=post_id_list)
    # 调整为正确的顺序v
    posts = sorted(posts, key=lambda post: post_id_list.index(post.id))

    # 组装 rank_data
    rank_data = []
    for post, (_, count) in zip(posts, cleaned_rank):
        rank_data.append([post, count])

        # # 思路三
        # post_id_list = [post_id for post_id, _ in cleaned_rank]
        # # post_dict = {
        # #     1: <Post: Post object>,
        # #     3: <Post: Post object>,
        # #     29: <Post: Post object>,
        # # }
        # post_dict = Post.objects.in_bulk(post_id_list)  # 批量获取 post 字典
        # for item in cleaned_rank:
        #     post_id = item[0]
        #     item[0] = post_dict[post_id]
        # rank_data = cleaned_rank

    return rank_data
