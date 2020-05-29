# -*- coding:utf-8 -*-
from __future__ import  unicode_literals  #统一所有字符串转为unicode类型
from django.contrib import admin
from account.models import User   #添加用户表


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'remark',
    )

admin.site.register(User,UserAdmin)  #admin站点添加注册用户功能