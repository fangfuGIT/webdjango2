# -*- coding: utf-8 -*-

# Author： fangfu

from django.db import models
from django.contrib.auth.models import User
from apps.permissions.Decoding import encode_decode



class CPUInfo(models.Model):
    id = models.AutoField('ID', primary_key=True, null=False)
    ipaddr = models.CharField('IP地址', max_length=15, null=False)
    cpu = models.CharField('cpu', max_length=10, null=False)
    status = models.CharField('健康状态', max_length=1, default=0, null=False)
    #
    # class Meta:
    #     permissions = (
    #         ('view_cpuinfo', 'can view cpuinfo'),
    #     )