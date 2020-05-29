"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin                  #导入admin包
from django.urls import path, re_path, include    #导入path,re_path,include 函数
from django.views.generic import RedirectView   #导入通用类视图RedirectView用于简单的 HTTP 重定向，
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),             #访问admin路径转发admin.site.urls
    path('favicon.ico', RedirectView.as_view(url=r'static/images/favicon.ico')),  #重定向
    path('', IndexPage.as_view()),              #路径根后空就调用首页视图
    re_path(r'^login/$', LoginView.as_view()),  #匹配login开头/结尾,调用LoginView视图
    re_path(r'logout/$', LogoutView.as_view()), #匹配有logout/结尾,调用LoginView视图
    path('cmdb/', include('cmdb.urls'))         #匹配cmdb,转发到cmdb.urls二级路由文件
]