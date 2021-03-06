"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve

from extra_apps import xadmin
from apps.users.views import LoginView, LogoutView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    # 登陆与注册
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # 机构相关
    path('org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),
    # 用户操作相关
    path('op/', include(('apps.operations.urls', 'operations'), namespace='op')),
    # usercenter
    path('usercenter/', include(('apps.users.urls', 'users'), namespace='usercenter')),

    # 课程相关
    path('courses/', include(('apps.courses.urls', 'courses'), namespace='courses')),
    # 配置上传文件的现实URL
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})

]
