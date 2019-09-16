from math import ceil

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from common import rds
from post.helper import page_cache, read_count, get_top_n
from post.models import Post, Comment, Tag
from user.helper import login_required, check_perm
from user.models import User


def index(request):
    return HttpResponse("Success")


@page_cache(3)
def post_list(request):
    # 分页
    # 总帖子数
    totals = Post.objects.count()
    # 每页帖子数
    per_page = 10
    # 总页数
    pages = ceil(totals / per_page)
    # 当前页码 默认1
    page = int(request.GET.get("page", 1))

    start = (page - 1) * per_page
    end = start + per_page

    posts = Post.objects.all().order_by("-id")[start:end]
    try:
        nickname = request.session.get("nickname")
        user = User.objects.get(nickname=nickname)

        return render(request, "bbs/post/post_list.html", {"posts": posts, "pages": range(pages), "user": user})

    except:
        return render(request, "bbs/post/post_list.html", {"posts": posts, "pages": range(pages)})


# 建贴
@login_required
@check_perm("add_post")
def create(request):
    if request.method == "POST":
        uid = request.session.get("uid")
        print(uid)
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect("/post/read/?post_id=%s" % post.id)
    return render(request, "bbs/post/create_post.html")


# def add(request):
#     for i in range(33):
#         title = "奥特曼%s"% i
#         content = "难以忘记初次见你一双迷人的眼睛"
#         Post.objects.create(title=title, content=content)


# 读贴
@login_required
@page_cache(1)
@read_count
def read_post(request):
    post_id = int(request.GET.get("post_id"))
    post = Post.objects.get(id=post_id)
    uid = request.session.get("uid")
    user = User.objects.get(id=uid)
    return render(request, "bbs/post/read_post.html", {"post": post, "user": user})


#
#     return HttpResponse("创建成功")

# 删贴
@login_required
@check_perm("del_post")
def del_post(request):
    post_id = int(request.GET.get("post_id"))
    Post.objects.get(id=post_id).delete()
    rds.zrem("ReadRank", post_id)  # 同时删除排行数据
    return redirect("/")


# 改贴
@login_required
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        title = request.POST.get("title")
        content = request.POST.get("content")
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()

        # 标签
        str_tags = request.POST.get("tags")
        tag_names = [s.strip()
                     for s in str_tags.title().replace("，", ",").split(",")
                     if s.strip()]
        post.updata_tags(tag_names)
        return redirect("/post/read/?post_id=%s" % post.id)
    else:
        post_id = request.GET.get("post_id")
        post = Post.objects.get(id=post_id)
        # 将tag显示出来
        str_tags = ",".join(t.name for t in post.tags())
        return render(request, "bbs/post/edit_post.html", {"post": post, "tags": str_tags})


# 搜索
def search(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        posts = Post.objects.filter(content__contains=keyword)
        return render(request, "bbs/post/search.html", {"posts": posts})
    else:
        return render(request, "bbs/post/search.html")


# 排行
def top10(request):
    """
     rank_data = [
         [<Post(37)>, 128],
         [<Post(32)>,  96],
         [<Post(25)>,  89],
         [<Post(11)>,  71],
     ]
     """
    rank_data = get_top_n(10)
    return render(request, "bbs/post/top10.html", {"rank_data": rank_data})


# 评论
@login_required
@check_perm("add_comment")
def comment(request):
    # 评论
    uid = request.session.get("uid")
    post_id = request.POST.get("post_id")
    content = request.POST.get("content")
    Comment.objects.create(uid=uid, post_id=post_id, content=content)
    return redirect("/post/read/?post_id=%s" % post_id)


# 删除评论
@login_required
@check_perm('del_comment')
def del_comment(request):
    cid = request.GET.get("comment_id")
    comment = Comment.objects.get(id=cid)
    post_id = comment.post_id

    Comment.objects.get(id=cid).delete()
    return redirect('/post/read/?post_id=%s' % post_id)


# 标签
def tag_filter(request):
    tag_id = int(request.GET.get("tag_id"))
    tag = Tag.objects.get(id=tag_id)
    return render(request, "bbs/post/tag_filter.html", {"posts": tag.posts()})
