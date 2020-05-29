# -*- coding:utf-8 -*-
import json
from django.db.models import Q                  #Q查询方法执行多个字段搜索功能, 对关键字参数进行封装，从而更好地应用多个查询,组合使用&(and),|(or),~(not)操作符,当一个操作符是用于两个Q的对象,它产生一个新的Q对象
from django.http import QueryDict,JsonResponse  #后端获取前段数据放在QueryDict集中,JsonResponse返回Json格式
from django.views.generic import View, TemplateView  #View基于类视图，改造通用类视图成TemplateView get带传参data
from django.http import JsonResponse
from utils.baseviews import BaseAPIView, BaseListView #基于类视图BaseAPIView, BaseListView
from .models import Idc,Rack,Server             #基于数据表Idc,Rack,Server

class IdcView(BaseListView):                 #定义IdcView视图继承自基类视图BaseListView
    """机房的列表页/详情页，增删改查"""
    model = Idc                                 #模块表idc
    template_name = 'cmdb/idcs.html'            #模板即前端文件，根目录为templates/下, idc列表页
    template_detail = 'cmdb/idc_detail.html'    #idc详细页

    def get_queryset(self):                  #查询功能
        queryset = self.model.objects.all()    #导入对象所有查询记录
        search = self.request.GET.get('search') #search功能单独写函数, 前端页面传参内容做search,获取不到则为空
        if search:
            queryset = queryset.filter(Q(name__contains=search)|Q(address__contains=search)) #过滤条件包含或
        qs = [i.to_dict for i in queryset]      #如i在查询集内，i.to_dict格式化数据进字典，总进查询集列表
        return qs                           #返回查询集列表

class APIIdcView(BaseAPIView):              #定义接口页APIIdcView视图继承自基类视图BaseAPIView，只取数据用增删改
    """机房的API：查询"""
    model=Idc

class RackView(BaseListView):
    """机柜的列表页/详情页，增删改查"""
    model=Rack
    template_name='cmdb/racks.html'         #机柜列表页
    template_detail='cmdb/rack_detail.html' #机柜详细页

    def get_queryset(self):
        queryset=self.model.objects.all()
        idc_id=self.request.GET.get('idc_id')  #只取单字段idc_id
        if idc_id:
            queryset=queryset.filter(idc_id=idc_id)  #只取匹配idc_id所需记录
        search=self.request.GET.get('search')  #search功能单独写函数, 前端页面传参内容做search,获取不到则为空
        if search:  #过滤条件包含或
            queryset=queryset.filter(Q(name__contains=search)|Q(number__contains=search)|Q(size__contains=search))
        qs=[i.to_dict for i in queryset]      #如i在查询集内，i.to_dict格式化数据进字典，总进查询集列表
        return qs                             #返回查询集列表

class APIRackView(BaseAPIView):               #定义接口页
    """机柜的API：查询"""
    model=Rack

class ServerView(BaseListView):
    """服务器的列表页/详情页，增删改查"""
    model=Server
    template_name='cmdb/servers.html'
    template_detail='cmdb/server_detail.html'

    def get_queryset(self):
        queryset=self.model.objects.all()
        rack_id=self.request.GET.get('rack_id')
        if rack_id:
            queryset = queryset.filter(rack_id=rack_id)  # 只取匹配rack_id所需记录
        search = self.request.GET.get('search')
        if search:
            queryset=queryset.filter(Q(name__contains=search)|Q(ip__contains=search))
        qs=[i.to_dict for i in queryset]
        return qs

class APIServerView(BaseAPIView):
    """机柜的API：查询，自动采集的信息录入"""
    model=Server

    def post(self,request,*args,**kwargs):    #http.request.post方式获取数据，适合更新数据
        data=QueryDict(request.body).dict()   #从前端获取http.request的数据放到字典QueryDict
        name=data.get('hostname')             #字典取键值赋值
        uuid=data.get('uuid')
        server_type = data.get('server_type')
        cpu = data.get('server_cpu')
        memory = data.get('server_mem')
        disk = data.get('server_disk')
        daq = json.dumps(data)               #将dict转化成str格式
        server_data={                        #查询前端数据存字典data, 重组后存字典server_data
            'name': name,
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'uuid': uuid,
            'server_type': server_type,
            'daq': daq
        }
        qs_instance = self.model.objects.filter(uuid=uuid,server_type=server_type) #过滤条件
        if qs_instance: #如果数据已经存在则保存，不存在则创建，**server_data为引用字典指针
            qs_instance.update(**server_data)
            qs_instance.first().save()
        else:
            self.model.objects.create(**server_data)
        return JsonResponse({})   #post已经提交更新操作给前端，返回空字典

class DashBoardView(TemplateView):        #仪表盘列表页
    """DashBoard页面"""
    template_name = 'dashboard.html'

class APIDashBoardView(View):             #仪表盘详细页
    """DashBoard页面需要的数据"""
    def get(self,request,*args,**kwargs):   #http.request.get方式获取数据，适合仅获取不更新
        data={}                           #data空字典初始化
        data_idc_servers = []             #data_idc_servers 空列表初始化
        data_site = []                    #data_site空列表初始化
        idc_list = Idc.objects.all()      #Idc所有记录集
        for idc in idc_list:              #只要Idc在idc_list列表中
            servers = 0                   #server赋初值0
            site_idc = {}                 #site_idc空字典,每idc多少机位site
            racks = idc.rack_set.all()    #rack_set 每个idc机柜记录集
            total_site = racks.count()*10 #每机柜可放10台机位，机位总数
            for rack in racks:            #同一机柜，servers计数
                servers += rack.to_dict.get('servers').get('count')
            data_idc_servers.append(      #data_idc_servers列表追加元素，小列表idc名称和包含servers数
                [idc.name, servers]
            )
            if total_site > 0:                #机位总数>0, 机位启用
                site_idc['name'] = idc.name, #表idc字段name赋值列表元素name
                site_idc['total_site'] = total_site, #机位总数赋值列表元素
                site_idc['site'] = servers,  #server总数赋值列表元素
                data_site.append(site_idc)   #data_site列表追加元素
        data['data_idc_servers'] = data_idc_servers  #列表追加元素
        data['data_site'] = data_site
        data['count'] = {
            'idcs': idc_list.count(),
            'racks': Rack.objects.count(),
            'servers': Server.objects.count()
        }
        return JsonResponse({'data': data})   #返回大字典，键名data值data字典