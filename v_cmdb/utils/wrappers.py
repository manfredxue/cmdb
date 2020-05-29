# -*- coding:utf-8 -*-
'''
装饰器（decorator）对于受到封装的原函数来说，装饰器能够在那个函数执行前或者执行后分别运行一些代码，使得可以在装饰器里面访问并修改原函数的参数以及返回值，以实现约束定义、调试程序、注册函数等目标。装饰器一般返回一个包装器（wrapper），而functools.wraps就是装饰包装器的装饰器
'''
from functools import wraps    #引入wraps装饰器包
from django.http import JsonResponse

def handle_save_data(func):       #装饰器文件定义如何处理在保存数据时出现的异常原因
    @wraps(func)                  #调用装饰器函数wraps
    def wrapper(*args, **kwargs):
        try:                      #正常取值
            return func(*args, **kwargs)
        except Exception as e:    #如下情况触发异常
            code = e.args[0]      #异常原因的状态码
            desc = e.args[1]      #异常原因的描述
            if code == 1062:      #MySQL的Error_code为1062
                status = 0        #自定义python连接mysql正常0
                instance = '名称重复({})'.format(desc)  #字符串常规类型格式化
            else:
                status = -1      #python连接mysql异常-1
                instance = desc
            return JsonResponse({'data': instance, 'status':status})  #返回状态码和原因描述
    return wrapper