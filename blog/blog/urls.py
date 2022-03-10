"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts import views
from django.conf import settings
from django.conf.urls.static import static
from posts.check_me import check_user, login_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_user(views.login), name="login"),
    path('logout/',views.logout, name="logout"),
    path('register/',login_user(views.Register), name="register"),
    path('index/',views.index, name="index"),
    path('showlist/', views.showlist, name="showlist"),
    path('update/<slug>', views.updateview, name="update"),
    path('delete/<int:id>', views.deleteview, name="delete"),
    path('create/',check_user(views.createpost),name='createpost'),
    path('search/',views.searchview,name='search'),
    path('like/<int:id>', views.LikeView, name='likeview'),
    path('dislike/<int:id>', views.dislikeView, name='dislikeview'),
    path('comment/<int:id>', views.commentView, name='comment'),
    path('commentlike/<int:id>', views.commentlike, name='commentlike'),
    path('grouplist/',views.groupview,name="group"),
    path('show_group_list/<slug>', views.groupList, name='showgroup'),
    path('create_group/', views.create_group, name='creategroup'),
    path('follow/<int:id>',views.followView,name='follow'),
    path('unfollow/<int:id>',views.unfollowView,name='unfollow'),
    path('settings/',views.setting_view,name='settings'),
    path('admin_panel/<int:id>',views.adminView,name='admin_panel'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

