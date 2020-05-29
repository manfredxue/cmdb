from django.db import models    #从django.db导入模块models, 用在修改数据库
#from account.models import User
import json                     #导入json格式

class BaseModel(models.Model):  #定义公共虚拟表，BaseModel类在数据库内成抽象表，由别的表来继承。新表自己就不用设这些字段。
    '''
        基础表(抽象类)
    '''
    name = models.CharField(default='', null=True, blank=True, max_length=128, verbose_name='名字')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    remark = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    @property                #装饰器在BaseModel类中
    def to_dict_base(self):  #定义字典基类并序列化成基础列表
        ret = dict()         #字典完整赋值变量ret
        for attr in [f.name for f in self._meta.fields]:  #如果f.name字段在所有元字段内，取f.name对象的attr属性
            value = getattr(self, attr)   #获取self对象的属性值
            ret[attr] = value             #赋值不同列表ret, 下标attr,值value
        return ret

    def __unicode__(self):   #美化打印
        return self.name

    class Meta:          #嵌套类，给上级类定义功能
        abstract = True  #抽象类，是为了继承，将该基类定义为抽象类，即不必生成数据库表单，只作为一个可以继承的基类，把一些子类必须的代码放在基类，避免重复代码也避免重复录入数据库
        ordering = ['-id'] #按id倒序


class Idc(BaseModel):   #IDC类继承自BaseModel类，类即为数据表
    address = models.CharField(max_length=256, verbose_name='地址')  #再添加字段

    class Meta:
        ordering=['-id']
        unique_together = ('name',)  #联合约束指在这个表中，每一行的name字段必须唯一，不能重复

    @property
    def to_dict(self):  #定义字典类并序列化为rack列表
        ret = self.to_dict_base #引用基类字典
        objects = self.rack_set.all() #导入所有rack记录集
        #相同机柜rack的data数据和计数值组成字典键值对存到列表ret['rack']中
        ret['racks'] = {'data': [obj for obj in objects.values()], 'count': objects.count()}
        return ret


class Rack(BaseModel):   #rack类继承自BaseModel类，类即为数据表
    #rack表的idc字段外键关联到idc表字段idc_id, 外键属性on_delete为models.SET_DEFAULT,外表idc删除记录时本地rack表的外键idc_id置默认值为空
    idc = models.ForeignKey(Idc, default='', null=True, blank=True, on_delete=models.SET_DEFAULT,verbose_name='所属机房')
    number = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='编号')
    size = models.CharField(default='', max_length=8, null=True, blank=True, verbose_name='U型')

    class Meta:
        ordering = ['-id']
        unique_together = ('name','idc')

    @property
    def to_dict(self):    #定义字典类并序列化为server列表
        ret = self.to_dict_base  #引用基类字典
        idc = getattr(self,'idc') #获得对象self的idc属性值
        idc_data = idc.to_dict if idc else {}   #取出对应idc记录,否则为空字典
        ret['idc'] = idc_data #存入列表ret['idc'], 下标idc, 值为记录
        objects = self.server_set.all() #导入所有server记录集
        #相同机柜server的data数据和计数值组成字典键值对存到列表ret['servers']中
        ret['servers']={'data':[obj for obj in objects.values()], 'count': objects.count()}
        return ret


class Server(BaseModel): #server类继承自BaseModel类，类即为数据表
    STATUS = (           #添加字段STATUS
        (0,u'下线'),     #下划线选择项
        (1,u'在线'),
    )
    rack = models.ForeignKey(Rack, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机柜')
    uuid = models.CharField(default='', max_length=128, null=True, blank=True,verbose_name='UUID')
    cpu = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='内存')
    disk = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='磁盘大小')
    ip = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='ip地址')
    business = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='业务线')
    server_type = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='服务器类型')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='运行状态')

    class Meta:
        ordering =  ['-id']
        unique_together = ('uuid', 'server_type')  #联合约束指在这个表中，每一行的uuid字段server_type字段必须唯一，不能重复

    @property
    def to_dict(self):  #定义字典类并序列化为数据采集daq列表
        ret = self.to_dict_base  #引用基类字典
        rack = getattr(self, 'rack')  #获得对象self的rack属性值
        rack_data = rack.to_dict if rack else {}  #取出对应rack记录,否则为空字典
        ret['rack']= rack_data   #存入列表ret['rack'], 下标idc, 值为记录
        daq=eval(self.daq) if self.daq else ''   #eval函数返回self.daq字符串表达式值
        ret['daq'] = daq                      #存入列表ret['daq'], 下标daq, 值为记录
        ret['daq_jason'] = json.dumps(daq)    #json.dumps将dict类型转化为str类型,存入列表ret['daq_jason'],
        return ret
    

