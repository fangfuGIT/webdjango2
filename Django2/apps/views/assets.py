# -*- coding: utf-8 -*-

# Author： fangfu

from rest_framework import viewsets, permissions
from apps.models import IDCInfo, ServerInfo, DataBaseInfo, CpuInfo
from apps.serializers import IDCSerializer, DataBaseSerializer, ServerSerializer, CpuSerializer, PermissionsControll, UserSerializer
from django.contrib.auth.models import User

from django.views.generic import ListView

from guardian.mixins import PermissionListMixin


class CpuViewsets(viewsets.ModelViewSet):
    #queryset = serverinfo.objects.all()
    serializer_class = CpuSerializer
    queryset = CpuInfo.objects.all()
    permission_classes = (permissions.AllowAny, PermissionsControll)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class ServerViewsets(viewsets.ModelViewSet):
    #queryset = serverinfo.objects.all()
    serializer_class = ServerSerializer
    queryset = ServerInfo.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DataBaseViewsets(viewsets.ModelViewSet):
    serializer_class = DataBaseSerializer
    queryset = DataBaseInfo.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IDCViewsets(viewsets.ModelViewSet):
    queryset = IDCInfo.objects.all()
    serializer_class = IDCSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#
# class TaskViewsets(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


class UserViewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)


class UserDetailsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)





# class TaskDetailViews(PermissionListMixin, ListView):
#     model = Task
#     permission_required = ['view_task', ]
