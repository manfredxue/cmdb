# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import  AbstractUser   #引入AbstractUser类用于继承
class User(AbstractUser):   #自定义User类表替换系统User表
    ROLES=(
        ('1',u'总监'),
        ('2', u'经理'),
        ('3', u'研发'),
    )
    role=models.CharField(max_length=32,default='developer',choices=ROLES)
    remark=models.CharField(max_length=128,default='',blank=True)

    class Meta:                  #定义元数据，任何不是字段数据
        verbose_name_plural=u'用户'

    def __unicode__(self):       #美化打印
        return self.username