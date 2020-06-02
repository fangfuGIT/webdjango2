"""apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from apps import view
from apps.views import execute, test_view
from apps.views.execute import call_ansible
from apps.views.execute import call_shell
#from apps.views import enforce
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token


from apps.views import assets
import apps.test

from django.contrib.auth.views import login, logout

router = DefaultRouter()
router.register('server', assets.ServerViewsets)
router.register('idc', assets.IDCViewsets)
#router.register('task', assets.TaskViewsets)
router.register('database', assets.DataBaseViewsets)
router.register('cpu', assets.CpuViewsets)

#router.register('ssh', view.sysinit)
#router.register('userlist', views.UserViewsets)
#router.register('userdetail', views.UserDetailsets)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_jwt_token),
    path('user/', include('rest_framework.urls', namespace='rest_framework')),
    #path('login/', view.user_login),
    path('form/', view.new_topic),
    path('slogin/', view.login_index),
    path('doc/', include_docs_urls(title='doc')),
    path('ssh/', call_shell.ssh_server),
    path('shell/', call_shell.call_script),
    path('ansible/', call_ansible.call_command),
    path('yml/', call_ansible.call_yml),
    #path('goodyml/', view.test),
    path('echo_once/', view.echo_once),
    path('once/', view.oncee),
    path('call_init_yml/', call_ansible.call_init_yml),
    path('sysinit/', view.sysinit),
    path('call_openarea/', call_ansible.call_openarea),
    path('openarea/', view.openarea),

    path('received_sys_info/', test_view.received_sys_info),

    path('index/', view.index),
    path('login/', view.DefineLoginView.as_view()),
    path('logout/', view.DefineLogoutView.as_view()),
    path('dbinit/', view.dbinit),
    path('resinit/', view.resinit),

    path('blank/', view.blank),
    path('blank_bak/', view.blank_bak),
   # path('login/', view.login),
    path('buttons/', view.buttons),
    path('flot/', view.flot),
    path('forms/', view.forms),
    path('grid/', view.grid),
    path('icons/', view.icons),
    path('morris/', view.morris),
    path('notifications/', view.notifications),
    path('panelswells/', view.panelswells),
    path('tables/', view.tables),
    path('typography/', view.typography),
    path('user/list/', view.userlist),
    path('add_svn_repo/', view.add_svn_repo),
    path('create_idc/', view.create_idc),
    path('list_idc/', view.list_idc),
    path('repo_add/', view.repo_add),
    path('repo_edit/', view.repo_edit),
    path('repo_list/', view.repo_list),
    path('repo_deploy/', view.repo_deploy),
    path('repo_del/', view.repo_del),


    path('loginn/', view.loginn),
    path('socket/', view.client_socket),






    #path('plat/', views.plat),
    #re_path(r'^ssh/$')
    #re_path(r'^ssh/(.+)/$', views.sshserver),
    #path('tt/', views.TaskDetailViews.as_view(), name="list"),
    #path('task/', views.TaskViewsets.as_view()),
    # path('', views.http_index),
  #  path('index/', view.index),
    path('indexx/', view.indexx),
    path('time/', view.time),
    # path('admin/', admin.site.urls),
    # path('userlist/', views.UserList.as_view()),
    # #path('serverlist/', views.ServerList.as_view()),
    # path('server/', views.ServerViewsets.as_view({'get': 'list'}), ({'post': 'create'})),
]




