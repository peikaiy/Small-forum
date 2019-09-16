"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

from post import views as post_views
from user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^xadmin/', admin.site.urls),
    # url(r'^post/', include("post.urls", namespace="post")),
    url(r'^index/', post_views.index, ),

    url(r'^$', post_views.post_list),

    # post
    url(r'^post/list/', post_views.post_list, name="list"),
    url(r'^post/read/', post_views.read_post, name="read"),
    url(r'^post/edit/', post_views.edit_post, name="edit"),
    url(r'^post/create/', post_views.create, name="create"),
    url(r'^post/search/', post_views.search, name="search"),
    url(r'^post/top10/', post_views.top10, name="top10"),
    url(r'^post/comment/', post_views.comment, name="comment"),
    url(r'^post/del_comment/', post_views.del_comment, name="del_comment"),
    url(r'^post/tag/', post_views.tag_filter, name="tag"),
    url(r'^post/del_post/', post_views.del_post, name="del_post"),
    # url(r'^add/', post_views.add, name="search"),

    # user
    url(r'^user/register/', user_views.register, name="register"),
    url(r'^user/login/', user_views.login, name="login"),
    url(r'^user/logout/', user_views.logout, name="logout"),
    url(r'^user/user_info/', user_views.user_info, name="user_info"),

    #   medias文件 static静态文件
    # url(r'^medias/(?P<path>.*)$', serve, {'document_root': '/home/peikaiy/BBS/medias'}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': '/home/peikaiy/BBS/static'}),
    url(r'^medias/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^user/create_perms/', user_views.create_perms, name="create_perms"),
    url(r'^user/create_role/', user_views.create_role, name="create_role"),
    url(r'^user/to_user_role/', user_views.to_user_role, name="to_user_role"),
    url(r'^user/to_role_perm/', user_views.to_role_perm, name="to_role_perm"),

]

# 全局404页面配置
handler404 = 'Nav_views.pag_not_found'
# （handler404 = "你的app.views.函数名"）
# 全局500页面配置
handler500 = 'Nav_views.page_error'

# media静态文件
# media 路径配置
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
