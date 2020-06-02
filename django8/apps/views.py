# -*- coding: utf-8 -*-

# Author： fangfu

#
# from rest_framework.viewsets import ModelViewSet
# from apps.serializers import *
#
# class CpuInfoView(ModelViewSet):
#     queryset = CPUInfo.objects.all()
#     serializer_class = CpuInfoSerializer


from rest_framework import viewsets
from apps.serializers import CpuInfoSerializer
from apps.models import CPUInfo

class CpuViewSet(viewsets.ModelViewSet):
    queryset = CPUInfo.objects.all()
    serializer_class = CpuInfoSerializer