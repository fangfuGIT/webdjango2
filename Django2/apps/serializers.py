#from django.test import TestCase

# Create your tests here.


# from django.shortcuts import render, redirect
from apps.models import IDCInfo, ServerInfo, DataBaseInfo, CpuInfo
from rest_framework import serializers
from rest_framework import permissions
from django.contrib.auth.models import User


#from apps.models import userinfo, Snippet


#
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     # 利用字段标志控制序列化器渲染到HTML页面时的的显示模板
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#
#     # 给定经过验证的数据，创建并返回一个新的 Snippet 实例
#     def create(self, validated_data):
#         return Snippet.objects.create(**validated_data)
#
#     # 给定经过验证的数据，更新并返回一个已经存在的 Snippet 实例
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance


# class UserSerializers(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     user = serializers.CharField(read_only=True)
#     password = serializers.CharField(read_only=True)
#     email = serializers.EmailField(read_only=True)
#
#     def create(self, validated_data):
#         return userinfo.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.user = validated_data.get('user', instance.user)
#         instance.password = validated_data.get('password', instance.password)
#         instance.email = validated_data.get('email', instance.email)
#         instance.save()
#         return instance
class IDCSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = IDCInfo
        fields = '__all__'


class CpuSerializer(serializers.ModelSerializer):
   # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = CpuInfo
        fields = '__all__'



class ServerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ServerInfo
        fields = '__all__'
      #  fields = ('id', 'server_name', 'system', 'type', 'server_ip', 'owner')


class DataBaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = DataBaseInfo
        fields = '__all__'


# class TaskSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     # reported_by = serializers.ModelSerializer(source="reported_by.username")
#
#     class Meta:
#         model = Task
#         fields = ('id', 'title',  'content', 'owner', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    #snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = '__all__'
        #fields = ('id', )


class PermissionsControll(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #if request.method in permissions.IsAuthenticated:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user



from guardian.shortcuts import assign_perm
from django.contrib.auth.models import User

# class PermissionsControll(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if






# def login(self, request):
#     if request.method == "GET":
#         return render(request, "login.html")
#
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#
#         user = userinfo.objects.filter(user=username, password=password)
#         if user:
#             # return render(request, 'index.html', {'username': username})
#             return redirect('/index', {'username': username})
#         else:
#             # return HttpResponse("wrong")
#             return render(request, 'login.html')

