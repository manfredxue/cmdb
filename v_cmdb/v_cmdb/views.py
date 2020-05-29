# coding=utf-8
from django.views.generic import View, TemplateView             #View基于类视图，改造通用类视图成TemplateView get带传参data
from django.contrib.auth import authenticate, login, logout     #导入authenticate, login, logout模块
from django.http import HttpResponseRedirect                    #Http逻辑处理后转到其他页面修改再重定向到前端
from django.http.response import JsonResponse                   #后端获取前段数据放在QueryDict集中,JsonResponse返回Json格式
from django.contrib.auth.mixins import LoginRequiredMixin       #验证登录用户类型和权限
from account.models import User                                 #导入加强版用户表
from utils.ldaptools import LdapOps                             #从utils.ldaptools导入自定义LdapOps模块

class LoginView(TemplateView):
    """登录页面, 用户密码鉴权"""
    template_name = 'login.html'                               #模板即前端文件，根目录为templates/下, login登录验证页

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        login_type = request.POST.get('login_type', None)
        if login_type == 'ldap':                              #ldapcheckox如选中，区分是否ldap登录
            ldap_ops = LdapOps()                              #调用类生成实例
            res = ldap_ops.check(username, password)          #check方法验证LDAP鉴权
            status = res.get('status')                        #取出状态码
            if status == 0:  # LDAP验证通过
                try:  # 用户存在，改密码
                    user = User.objects.get(username=username)
                except User.DoesNotExist:  # 用户不存在，创建用户
                    user = User.objects.create_user(username=username, password=password)
                user.set_password(password)
                user.save()
            else:
                data = res.get('data')
                return JsonResponse({'status': status, 'data': data})   #返回LDAP server端
        user = authenticate(username=username, password=password)  # django鉴权
        if user is not None:  # 用户密码及token正确
            login(request, user)
            status = 0
        else:
            status = 1
        return JsonResponse({'status': status})


class LogoutView(LoginRequiredMixin, View):
    """"退出登录"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")


class IndexPage(LoginRequiredMixin, TemplateView):
    """首页"""
    template_name = 'index.html'

'''
子类HttpResponseRedirect
当一个逻辑处理完成后，不需要向客户端呈现数据，而是转回到其它页面，如添加成功、修改成功、删除成功后显示数据列表，而数据的列表视图已经开发完成，此时不需要重新编写列表的代码，而是转到这个视图就可以，此时就需要模拟一个用户请求的效果，从一个视图转到另外一个视图，就称为重定向。
Django中提供了HttpResponseRedirect对象实现重定向功能，这个类继承自HttpResponse，被定义在django.http模块中，返回的状态码为302。
'''