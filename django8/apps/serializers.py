# -*- coding: utf-8 -*-

# Author： fangfu

#
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from apps.models import CPUInfo
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
# class BlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CPUInfo
#         fields = ('id', 'ipaddr', 'cpu', 'status')



from rest_framework import serializers
from apps.models import CPUInfo


class CpuInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUInfo
        fields = ('id', 'ipaddr', 'cpu', 'status')

