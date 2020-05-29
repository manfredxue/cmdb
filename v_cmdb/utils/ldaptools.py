# -*- coding:utf-8 -*-
import ldap  #引用python-ldap库
from django.conf import settings #引用django配置文件中设置对象

class LdapOps(object):            #定义LdapOps函数

    locals().update(settings.LDAP)
    ret = {}                     #空字典初始化

    def check(self, ldap_user, ldap_password):   #定义装饰器函数
        uri = "ldap://{}:{}".format(self.host, self.port)  #ldap路径+格式化过主机+端口建立连接
        conn = ldap.initialize(uri)  #初始化ldap连接
        try:
            conn.simple_bind_s(ldap_user, ldap_password)  #连接使用简单绑定用户：用户名，密码
            status = 0        #登录正常
        except Exception as e:
            status = 2        #登录失败
            self.ret["data"] = e.args[0]  #异常原因
        self.ret["status"]  = status      #状态码
        return self.ret










