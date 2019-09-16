from django.db import models

# Create your models here.
from user.models import User


#   帖子
class Post(models.Model):
    uid = models.IntegerField(default=6)
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if not hasattr(self, "_auth"):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comments(self):
        return Comment.objects.filter(post_id=self.id).order_by("-id")

    def tags(self):
        # 查找tag
        relations = PostTagRelation.objects.filter(post_id=self.id).only("tag_id")
        # print("查找标签",relations)
        tag_id_list = [r.tag_id for r in relations]
        return Tag.objects.filter(id__in=tag_id_list)

    def updata_tags(self, tag_names):
        Tag.ensure_tags(tag_names)

        # 去除已存在的tag 选出需要新创建的tag-name
        updata_names = set(tag_names)
        exist_names = {t.name for t in self.tags()}

        # 筛选出需要新创建的关系
        need_create_names = updata_names - exist_names
        PostTagRelation.add_post_tags(self.id, need_create_names)

        # 筛选出需要删除的关系
        need_delete_names = exist_names - updata_names
        PostTagRelation.del_post_tags(self.id, need_delete_names)


#   评论
class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    # 对应用户 属性
    @property
    def auth(self):
        if not hasattr(self, "_auth"):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    # 对应帖子 属性
    @property
    def post(self):
        if not hasattr(self, "_post"):
            self._post = Post.objects.get(id=self.post_id)
        return self._post


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    @classmethod
    def ensure_tags(cls, tag_names):
        # 确保传入的name存在
        tags = cls.objects.filter(name__in=tag_names).only("name")
        exist_names = [t.name for t in tags]
        need_create = [cls(name=name) for name in tag_names if name not in exist_names]
        # 批量创建不存在的tag
        cls.objects.bulk_create(need_create)

    def posts(self):
        # 查找帖子
        relations = PostTagRelation.objects.filter(tag_id=self.id).only("post_id")
        # print("查找帖子",relations)
        post_id_list = [r.post_id for r in relations]
        return Post.objects.filter(id__in=post_id_list)


# post和tag之间的关系表
class PostTagRelation(models.Model):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    # 给帖子添加tag
    @classmethod
    def add_post_tags(cls, post_id, tag_names):
        # 根据name取出id
        tag_id_list = [t.id for t in Tag.objects.filter(name__in=tag_names)]
        # 创建帖子
        relations = [cls(post_id=post_id, tag_id=tid) for tid in tag_id_list]
        cls.objects.bulk_create(relations)

    # 删除帖子tag
    @classmethod
    def del_post_tags(cls, post_id, tag_names):
        tag_id_list = [t.id for t in Tag.objects.filter(name__in=tag_names)]
        cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()
