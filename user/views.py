from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user.models import User, Role, Permission, UserRoleRelation, RolePermRelation

# Create your views here.
from user.forms import RegisterForm
from user.helper import login_required
from user.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            UserRoleRelation.add_role_to_user(user.id, "user")

            request.session["uid"] = user.id
            request.session["nickname"] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect("user_info")
        else:
            return render(request, "bbs/user/register.html", {"error": form.errors})
    return render(request, "bbs/user/register.html")


# 登陆
def login(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        try:
            user = User.objects.get(nickname=nickname)

        except:
            return render(request, "bbs/user/login.html", {"error": "没有此用户"})
        if user:
            if check_password(password, user.password):
                request.session["uid"] = user.id
                request.session["nickname"] = user.nickname
                # 头像
                request.session['avatar'] = user.avatar
                print(user.avatar)
                print("ok")
                return redirect("list")

            else:
                return render(request, "bbs/user/login.html", {"error": "密码错误"})

    return render(request, "bbs/user/login.html")


# 退出
@login_required
def logout(request):
    request.session.flush()
    return redirect("login")


# 个人信息
@login_required
def user_info(request):
    nickname = request.session.get("nickname")
    user = User.objects.get(nickname=nickname)
    return render(request, "bbs/user/user_info.html", {"user": user})


from user.models import User, Role, Permission, UserRoleRelation, RolePermRelation


# 创建权限
def create_perms(request):
    perms = [Permission(name="add_post"), Permission(name="del_post"), Permission(name="add_comment"),
             Permission(name="del_comment"), Permission(name="del_user")]
    Permission.objects.bulk_create(perms)
    return redirect("create_role")


# 创建角色
def create_role(request):
    Role.objects.bulk_create(
        [
            Role(name="admin"),
            Role(name="manager"),
            Role(name="user"),
        ])
    # return redirect("to_user_role")
    return redirect("to_user_role")


# 给用户分配角色
def to_user_role(request):
    # ying = User.objects.get(nickname = "影")
    # ru = User.objects.get(nickname = "如")
    us = User.objects.get(nickname="秋叶")

    # UserRoleRelation.add_role_to_user(ying.id, "admin")
    # UserRoleRelation.add_role_to_user(ru.id, "manager")
    UserRoleRelation.add_role_to_user(us.id, "user")
    return redirect("to_role_perm")


# # 给角色添加权限
def to_role_perm(request):
    admin = Role.objects.get(name="admin")
    manager = Role.objects.get(name="manager")
    user = Role.objects.get(name="user")
    # admin
    RolePermRelation.add_perm_to_role(admin.id, "del_user")
    RolePermRelation.add_perm_to_role(admin.id, "del_post")
    RolePermRelation.add_perm_to_role(admin.id, "del_comment")
    # manager
    RolePermRelation.add_perm_to_role(manager.id, "del_comment")
    RolePermRelation.add_perm_to_role(manager.id, "del_post")
    RolePermRelation.add_perm_to_role(manager.id, "add_post")
    RolePermRelation.add_perm_to_role(manager.id, "add_comment")
    # user
    RolePermRelation.add_perm_to_role(user.id, "add_comment")
    RolePermRelation.add_perm_to_role(user.id, "add_post")
    return HttpResponse("给角色添加权限成功")


"""
    权限分配
        add_post 发表帖子
        del_post 删除帖子
        add_comment 发表评论
        del_comment 删除评论
        del_user 删除用户
"""
# #
# # # 创建权限
# from user.models import User, Role, Permission, UserRoleRelation, RolePermRelation
# def create_perms(request):
#
#     perms = [Permission(name="add_post"), Permission(name="del_post"), Permission(name="add_comment"), Permission(name="del_comment"), Permission(name="del_user"),]
#     Permission.objects.bulk_create(perms)
#     return HttpResponse("创建权限成功")
#

# # 创建角色
# def create_role(request):
#     Role.objects.bulk_create([Role(name="admin"), Role(name="manager"), Role(name="user"),])
#     return HttpResponse("创建角色成功")
# #
# # # 给用户分配角色
# def to_user_role(request):
#     ying = User.objects.get(nickname = "影")
#     ru = User.objects.get(nickname = "如")
#     sha = User.objects.get(nickname = "木")
#
#
#     UserRoleRelation.add_role_to_user(ying.id, "admin")
#     UserRoleRelation.add_role_to_user(ru.id, "manager")
#     UserRoleRelation.add_role_to_user(sha.id, "user")
#     return HttpResponse("给用户分配角色成功")
#
# # # 给角色添加权限
# def to_role_perm(request):
#     admin = Role.objects.get(name="admin")
#     manager = Role.objects.get(name="manager")
#     user = Role.objects.get(name="user")
#     # admin
#     RolePermRelation.add_perm_to_role(admin.id, "del_user")
#     RolePermRelation.add_perm_to_role(admin.id, "del_post")
#     RolePermRelation.add_perm_to_role(admin.id, "del_comment")
#     # manager
#     RolePermRelation.add_perm_to_role(manager.id, "del_comment")
#     RolePermRelation.add_perm_to_role(manager.id, "del_post")
#     RolePermRelation.add_perm_to_role(manager.id, "add_post")
#     RolePermRelation.add_perm_to_role(manager.id, "add_comment")
#     # user
#     RolePermRelation.add_perm_to_role(user.id, "add_comment")
#     RolePermRelation.add_perm_to_role(user.id, "add_post")
#     return HttpResponse("给角色添加权限成功")
