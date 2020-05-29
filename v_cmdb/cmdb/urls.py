# -*- coding:utf-8 -*-
from django.conf.urls import url  #Django1.x版本写法
#URL配置(URLconf)就像Django 所支撑网站的目录。它的本质是URL与要为该URL调用的视图函数之间的映射表。
from .views import *
#循环urlpatterns，找到对应的函数执行,匹配上一个路径就找到对应的函数执行，就不再往下循环了，并给函数传一个参数request，和wsgiref的environ类似，就是请求信息的所有内容
urlpatterns = [
    url(r'^idcs/(?P<pk>\d+)?/?$', IdcView.as_view(), name='idcs'),                           #IDC列表页
    url(r'^api_idcs/(?P<pk>\d+)?/?$', APIIdcView.as_view(), name='api_idcs'),                #IDC接口页
    url(r'^racks/(?P<pk>\d+)?/?$', RackView.as_view(), name='racks'),                        #机柜列表页
    url(r'^api_racks/(?P<pk>\d+)?/?$', APIRackView.as_view(), name='api_racks'),             #机柜接口页
    url(r'^servers/(?P<pk>\d+)?/?$', ServerView.as_view(), name='servers'),                  #服务器列表页
    url(r'^api_servers/(?P<pk>\d+)?/?$', APIServerView.as_view(), name='api_servers'),       #服务器接口页
    url(r'^dashboard/(?P<pk>\d+)?/?$', DashBoardView.as_view(), name='dashboard'),           #仪表盘列表页
    url(r'^api_dashboard/(?P<pk>\d+)?/?$', APIDashBoardView.as_view(), name='api_dashboard'),#仪表盘接口页
]