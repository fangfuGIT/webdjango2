from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from apps.permissions.Decoding import encode_decode
import hashlib



class CpuInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, verbose_name="ID")
    ipaddr = models.CharField(max_length=16, null=False, verbose_name="IP地址")
    cpu = models.CharField(max_length=50, null=False, verbose_name="cpu值")
    status = models.CharField(max_length=50, null=False, verbose_name="健康状态")
    owner = models.ForeignKey(User, default="fangfu", on_delete=models.CASCADE)
    class Meta:
        permissions = (
            ('view_cpuinfo', 'can view cpuinfo'),
        )


class IDCInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, verbose_name="ID")
    name = models.CharField(max_length=50, null=False, verbose_name="机房名称")
    position = models.CharField(max_length=50, null=False, verbose_name="机房位置")
    status = models.CharField(max_length=50, null=False, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:   #内部类，定义一些Django模型类的行为特性
       # ordering = ('id',)   #ordering 返回结果依照哪个字段进行排序
        permissions = (
            ('view_idcinfo', 'can view idcinfo'),
        )


class ServerInfo(models.Model):
    id = models.AutoField('ID', primary_key=True, null=False)
    ipaddr = models.CharField('IP地址', max_length=15, null=True)
    username = models.CharField('用户名', max_length=10, null=True)
    password = models.CharField('密码', max_length=100, null=True)
    port = models.CharField('端口', max_length=5, null=False, default=22)
    keyfile = models.SmallIntegerField('密钥', blank=True, null=True)
    servername = models.CharField('服务器名称', max_length=50, null=False)
    system = models.CharField('操作系统', max_length=30, null=False)
    role = models.CharField('服务器用途', max_length=50, null=True)
    project = models.CharField('所属项目', max_length=50, null=True)
    owner = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.password = encode_decode.encode(self.password)
        # self.password = self.password.encode("utf8")
        # self.password = hashlib.md5(self.password).hexdigest()
        super(ServerInfo, self).save(*args, **kwargs)

    class Meta:
        permissions = (
            ('view_serverinfo', 'can view serverinfo'),
        )


class DataBaseInfo(models.Model):
    id = models.AutoField('ID', primary_key=True, null=False)
    project = models.CharField('所属项目', max_length=50, null=True)
    ipaddr = models.CharField('IP地址', max_length=15, null=True)
    username = models.CharField('MySQL用户名', max_length=10, null=True)
    password = models.CharField('MySQL密码', max_length=100, null=True)
    port = models.CharField('MySQL端口', max_length=5, null=False, default=3306)
    owner = models.ForeignKey(User, default="", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.password = encode_decode.encode(self.password)
        super(DataBaseInfo, self).save(*args, **kwargs)

    class Meta:
        permissions = (
            ('view_DataBaseInfo', 'can view DataBaseInfo'),
        )



class RepoUpgrade(models.Model):
    source_choice = (
        ('svn', 'svn'),
        ('git', 'git')
    )
    repo_type = (
        ("前端", "前端"),
        ("后端", "后端"),
        ("接口", "接口"),
    )
    repo_name = models.CharField(u"项目名称", max_length=100)
    repo_desc = models.CharField(u"项目描述", max_length=255, null=True, blank=True)
    repo_type = models.CharField(u"项目类型", choices=repo_type, max_length=30, null=True, blank=True)
    repo_source_type = models.CharField(u"版本库类型", max_length=5, choices=source_choice)
    repo_source_address = models.CharField(u"库地址", max_length=200)
    repo_user = models.CharField(u"库用户名", max_length=50, blank=False)
    repo_password = models.CharField(u"库密码", max_length=50, blank=True)
    server_path = models.CharField(u"远程部署路径", max_length=50)
    server_ip = models.CharField(u"远程服务器IP", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)









