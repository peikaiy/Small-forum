
from django.shortcuts import redirect, render

# 登录状态检查
from user.models import User


def login_required(view_func):
    def wrapper(request):
        uid = request.session.get("uid")
        if uid is None:
            return redirect("/user/login/")
        else:
            return view_func(request)

    return wrapper


# 权限检查
def check_perm(perm_name):
    def deco(view_func):
        def wrapper(request):
            uid = request.session["uid"]
            user = User.objects.get(id=uid)

            if user.has_perm(perm_name):
                return view_func(request)
            else:
                return render(request, "bbs/post/blockers.html")
        return wrapper
    return deco
