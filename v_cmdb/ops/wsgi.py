"""
WSGI config for ops project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
Web服务器网关版接口（Python Web Server Gateway Interface，缩写为WSGI）是为Python语言定义的Web服务器和Web应用程序或框架之间的一种简单权而通用的接口。
"""

import os           #导入标准库os,利用其中API

from django.core.wsgi import get_wsgi_application  #导入WSGI对象模块
#当WSGI服务器加载应用时，Django需要导入配置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ops.settings")  #在load model.XXX前设置默认ops/settings.py环境变量

application = get_wsgi_application()   #创建WSGI应用对象