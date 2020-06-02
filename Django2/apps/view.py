# -*- coding: utf-8 -*-

# Author： fangfu

from django.shortcuts import render, HttpResponse
import datetime
from django.views.generic import ListView

from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.auth.models import User
from guardian.mixins import PermissionListMixin

from apps.models import IDCInfo, ServerInfo
from apps.serializers import IDCSerializer, ServerSerializer, PermissionsControll
from apps.serializers import UserSerializer
from apps.permissions.ansible_api import Runner
from apps.permissions.paramiko import ssh_client, call_script
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.response import Response

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from apps.permissions.Decoding import encode_decode

from dwebsocket.decorators import accept_websocket

import paramiko
from django.conf import settings
from django.shortcuts import resolve_url

from django.contrib.auth.views import LoginView, LogoutView

import socket
from urllib import parse
from apps.models import RepoUpgrade
from django import forms





class RepoForm(forms.ModelForm):
    class Meta:
        model = RepoUpgrade
        fields = ['repo_name', 'repo_desc', 'repo_type', 'repo_source_type', 'repo_source_address', 'repo_user', 'repo_password', 'server_path', 'server_ip']
        widgets = {
            'repo_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'repo_desc': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'repo_type': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'repo_source_type': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'repo_source_address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'repo_user': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'repo_password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:450px'}),
            'server_path': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'server_ip': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }



def repo_list(request):
    result = RepoUpgrade.objects.all()
   # repo_name = result.values('repo_name')
    return render(request, 'repo_list.html', {"result": result.values('id', 'repo_name', 'repo_desc', 'repo_type', 'repo_source_type', 'repo_source_address', 'server_ip', 'created_at')})


def repo_del(request):
    id = request.GET.get("id")
    RepoUpgrade.objects.filter(id=id).delete()
    return repo_list(request)


def repo_edit(request):
    id=request.GET.get("id")
    case = RepoUpgrade.objects.get(id=id)
    if request.method == 'POST':
        form = RepoForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
        return repo_list(request)
    form = RepoForm(instance=case)
    return render(request, 'repo_edit.html', {'form': form})


def repo_deploy(request):
    return render(request, 'repo_deploy.html')


# def repo_edit(request):
#     id = request.GET.get("id")
#     RepoUpgrade.objects.filter(id=id).first()
#     if request.method == "POST":
#         repo_name = request.POST.get("repo_name")
#         repo_desc = request.POST.get("repo_desc")
#         repo_type = request.POST.get("repo_type")
#         repo_source_type = request.POST.get("repo_source_type")
#         repo_source_address = request.POST.get("repo_source_address")
#         repo_user = request.POST.get("repo_user")
#         repo_password = request.POST.get("repo_password")
#         server_path = request.POST.get("server_path")
#         server_ip = request.POST.get("server_ip")
#
#         RepoUpgrade.objects.filter(id=id).update(repo_name=repo_name, repo_desc=repo_desc, repo_type=repo_type,
#                                              repo_source_type=repo_source_type, repo_source_address=repo_source_address,
#                                              repo_user=repo_user, repo_password=repo_password, server_path=server_path,
#                                              server_ip=server_ip)
#     # return render(request, 'repo_edit.html', {"result": result.values('id', 'repo_name', 'repo_desc', 'repo_type', 'repo_source_type', 'repo_source_address', 'server_ip', 'created_at')})
#     context = {'form': form}
#     return render(request, 'repo_edit.html', context)



# def repo_edit(request, repo_id):
#     project = RepoUpgrade.objects.get(id=repo_id)
#  #   temp_name = "appconf/appconf-header.html"
#     if request.method == 'POST':
#         form = RepoForm(request.POST, instance=project)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('repo_list'))
#     else:
#         form = RepoForm(instance=project)
#     results = {
#         'form': form,
#         'project_id': repo_id,
#         'request': request,
#         'temp_name': temp_name,
#     }
#     return render(request, 'appconf/project_base.html', results)



# def project_list(request):
#     temp_name = "appconf/appconf-header.html"
#     all_project = Project.objects.all()
#     results = {
#         'temp_name': temp_name,
#         'all_project':  all_project,
#     }
#     return render(request, 'appconf/project_list.html', results)


def repo_add(request):
    """add new repo"""
    if request.method != 'POST':
        # didn't submit data: create a new form
        form = RepoForm  # RepoForm is imported from ./form.py
    else:
        # data submitted through post: process the data
        form = RepoForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect user to topics page
            return repo_list(request)
         #   return HttpResponseRedirect(reverse(''))
           # return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'repo_add.html', context)





import coreapi
@login_required
def create_idc(request):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://192.168.2.139:8000/doc/")

    # Interact with the API endpoint
    action = ["database", "create"]
    params = {
        "project": "2",
        "ipaddr": "2",
        "username": "2",
        "password": "eveuRbcf",
        "port": "1",
    }
    result = client.action(schema, action, params=params)
    return HttpResponse(result)



def list_idc(request):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://192.168.2.139:8000/doc/")

    # Interact with the API endpoint
    action = ["database", "list"]
    result = client.action(schema, action)
    return HttpResponse(result)




def client_socket(request):
    instr = 'hello'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.188', 6969))
  #  client.settimeout(5)
    cc = client.sendall(parse.quote(instr).encode('utf-8'))
    dd = 'adadfadsf'
    return HttpResponse(cc)







class DefineLoginView(LoginView):
    template_name = 'login.html'
    # def get_success_url(self):
    #     #url = self.get_redirect_url()
    #     username = self.request.POST.get('username')
    #     #return resolve_url(settings.LOGIN_REDIRECT_URL, {"username": username})
    #
    #     return render(self.request, 'index.html', {"username": user})
    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        return render(self.request, 'index.html', {"username": user})



class DefineLogoutView(LogoutView):
    template_name = 'login.html'


def add_svn_repo(request):
    return render(request, 'add_svn_repo.html')


# def once(request):
#     return render(request, "index.html")

@login_required
def sysinit(request):
    return render(request, "sysinit.html")


@login_required
def userlist(request):
    return render(request, 'userlist.html')

def login(request):
    return render(request, 'login.html')

@login_required
def index(request):
    return render(request, 'index.html')

def blank(request):
    return render(request, 'blank.html')

def dbinit(request):
    return render(request, 'dbinit.html')

def resinit(request):
    return render(request, 'resinit.html')

def blank_bak(request):
    return render(request, 'blank_bak.html')

def buttons(request):
    return render(request, 'buttons.html')

def flot(request):
    return render(request, 'flot.html')

def forms(request):
    return render(request, 'forms.html')

def grid(request):
    return render(request, 'grid.html')

def icons(request):
    return render(request, 'icons.html')

def morris(request):
    return render(request, 'morris.html')

def notifications(request):
    return render(request, 'notifications.html')

def panelswells(request):
    return render(request, 'panels-wells.html')

def tables(request):
    return render(request, 'tables.html')

def typography(request):
    return render(request, 'typography.html')


#@login_required
def openarea(request):
    return render(request, "openarea.html")

def oncee(request):
    command = '111'
    #command = request.POST.get('cmd')
   # request.websocket.send(exec_command(command))
    return HttpResponse(command)


def test(request):
    command = 'test'
    return HttpResponse(command)

def indexx(request):
        #password = request.COOKIES.get("password")
    return render(request, "index2.html")

def loginn(request):
    return render(request, "login2.html")



def exec_command(comm):
    hostname = '192.168.1.188'
    username = 'root'
    password = 'pwkj123'
    port = 22
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password, port=port)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.read()
    ssh.close()
    return result

@accept_websocket
def echo_once(request):
    if not request.is_websocket():
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index2.html')
    else:
        for message in request.websocket:
            if message != None:
                message = message.decode('utf-8')
                request.websocket.send(exec_command(message))
            else:
                request.websocket.send('命令为空，请重新输入！'.encode('utf-8'))


from apps.sysinit.form_test import User_Form
from django.urls import reverse

def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = User_Form()
    else:
        # POST 提交的数据，对数据进行处理
        form = User_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'login.html', context)


def user_login(request):
    username = request.GET.get('Username')
    password = request.GET.get('Password')
    user = auth.authenticate(username=username, password=password)
    if user and user.is_active:
        auth.login(request, user)
        request.session['Username'] = username
        return render(request, 'index.html')
        #return render(request, username)login
       # return HttpResponseRedirect('/', {"user": request.user})
    else:
       # if request.method == "POST":
            #return render(request, "用户名不存在或者密码错误")
        return render(request, 'login.html', {"login_error_info": "用户名不错存在，或者密码错误！"})
        #else:
        #    return render(request, 'login.html')


# def plat(request):
#     context = {}
#     return render(request, 'index.html', context)

def http_index(request):
    return render(request, "extend.html")

def login_index(request):
    return render(request, "login.html")

def response_index(request):
    return render(request, "index.html")
    #return redirect('/index')

def time(request):
    now = datetime.datetime.now()
    sstr = "time is: %s" % now
    return HttpResponse(sstr)

# def index(request):
#     if request.method == 'GET':
#         username = request.COOKIES.get("user")
#         #password = request.COOKIES.get("password")
#         return render(request, "index.html", {"username": username})

def sshserver(request):
    #command = "cat /etc/issue"
    command = request.POST.get('command')
    id = request.POST.get('id')
    #return HttpResponse(id)
    return ssh_client.ssh(id, command)

def callscript(request):
    id = request.POST.get('id')
    #return HttpResponse(id)
    return call_script.test_script(id)

def callansibleshell(request):
    # resource = {
    #     "webserver":
    #         [
    #             {"hostname": "183.61.x.x", "username": "root", "hostport": "16333", "password": "pwkj123"},
    #             {"hostname": "192.168.1.188", "username": "root", "hostport": "22", "password": "pwkj123"}
    #         ]
    # }
    # list=[]
    # for i in resource['webserver']:
    #     list.append(i["hostname"])

    id = request.POST.get('id')
    line = ServerInfo.objects.get(id=id)
    username = line.username
    pass_str = line.password
    password = encode_decode.decode(pass_str)
    port = line.port
    host = line.ipaddr

    args = request.POST.get('args')

    resource1 = {
        "webserver":
            [
                {"hostname": host, "username": username, "hostport": port, "password": password},
                {"hostname": "192.168.1.189", "username": "root1", "hostport": "22", "password": "pwkj123"}
            ]
    }




    rbt = Runner(resource1)
    rbt.run_adhoc(cdhosts=host, module='shell', args=args)
    #rbt.run_adhoc(cdhosts=["192.168.1.188"], module='shell', args='cat /etc/issue')


    run_result = rbt.get_multi_result()
    #run_result1 = rbt.get_alone_result()
    return JsonResponse(run_result)
    #return HttpResponse(run_result1)

def callansibleyml(request):
    resource = {
        "webserver":
            [
                {"hostname": "183.61.x.x", "username": "root", "hostport": "16333", "password": "pwkj123"},
                {"hostname": "192.168.1.188", "username": "root", "hostport": "22", "password": "pwkj123"}
            ]
    }
    list=[]
    for i in resource['webserver']:
        list.append(i["hostname"])

    rbt = Runner(resource)
    rbt.run_playbook(yml_path='1ff.yml')
    result = rbt.get_multi_result()
    return JsonResponse(result)


    #ip = request.POST.get('ip')
   # command = request.POST.get('args')
   #  list=[]
   #  for i in resource['webserver']:
   #      list.append(i["hostname"])
   # # return  HttpResponse(command)
   # # run = Runner(resource, command)
   #  rbt = Runner(resource)
    #rbt.run_adhoc(cdhosts=list, module='shell', args=command)
    #run_result = rbt.get_multi_result()
    #result = rbt.run_playbook(yml_path='ff1.yml')

    # result = rbt.run_adhoc(cdhosts=["192.168.1.188"], module='shell', args='cat /etc/issue')
    # run_result = rbt.get_multi_result()
    # run_result1 = rbt.get_alone_result()
    # return HttpResponse(run_result1)
    #return JsonResponse(run_result)

    #return HttpResponse(result)
#   return JsonResponse({'msg': str(result), "code": 200, 'data': []})

    #return JsonResponse({'error': result}, status=401)

  #  rbt.Playbook_Run(host=['192.168.1.188'], playbook_path='ff.yml')
  #  run_result = rbt.get_multi_result()
    # return json.dumps(run_result)
    #return Response(result)



#    return run.result()

# class UserList(APIView):
#     #def get(self, request, format=None):
#     def get(self, request):
#         ss = userinfo.objects.all()
#         serializer = UserSerializers(ss, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         dd = UserSerializers(data=request.data)
#         if dd:
#             UserSerializers.save()
#             return Response(dd.data, status=status.HTTP_201_CREATED)
#         return Response(dd.errors, status=status.HTTP_400_BAD_REQUEST)


# class ServerList(APIView):
#     def get(self, request):
#         gg = serverinfo.objects.all()
#         serializer = Serverserializer(gg, many=True)
#         return Response(serializer.data)

#
# class ServerList(generics.ListCreateAPIView):
#     queryset = serverinfo.objects.all()
#     serializer_class = Serverserializer
#
#
# class ServerDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = serverinfo.objects.all()
#     serializer_class = Serverserializer


# class ServerViewsets(generics.RetrieveUpdateDestroyAPIView):
#     queryset = serverinfo.objects.all()
#     serializer_class = ServerSerializer

class ServerViewsets(viewsets.ModelViewSet):
    #queryset = serverinfo.objects.all()
    serializer_class = ServerSerializer
    queryset = ServerInfo.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def form_create(self, ServerSerializer):
    #     ServerSerializer.save()

class IDCViewsets(viewsets.ModelViewSet):
    queryset = IDCInfo.objects.all()
    serializer_class = IDCSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, PermissionsControll)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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





























