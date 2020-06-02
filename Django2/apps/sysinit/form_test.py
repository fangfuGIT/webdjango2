# -*- coding: utf-8 -*-

# Author： fangfu



from django import forms
from django.contrib.auth.models import User
#from apps.models import ServerInfo


class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {'username': '请输入username'}


# class CForm(forms.ModelForm):
#     class Meta:
#         model = ServerInfo
#         fields = ['ipaddr']
#         labels = {'ipaddr': '请输入IP地址'}


# _*_ coding: utf-8 _*_
__author__ = 'fangfu'
__date__ = '2018/4/8 16:33'
# !/usr/bin/env python

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.inventory.host import Host


def add_dynamic_host(hosts_list):
    loader = None
    inventory = InventoryManager(loader=loader, sources=resource)
    for hosts in hosts_list:
        hostname = hosts.get("hostname")
        hostport = hosts.get("hostport")
        password = hosts.get("password")
        username = hosts.get("username")
        my_host = Host(name=hostname, port=hostport)
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_host', value=hostname)
        variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_pass', value=password)
        variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_port', value=hostport)
        variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_user', value=username)
        inventory.add_host(host=hostname, port=hostport)
        print()
    print(hosts_list)


resource = {"webserver": [{"hostname": "192.168.2.236", "username": "root", "hostport": "22", "password": "pwkj123"},
                          {"hostname": "192.168.2.234", "username": "root", "hostport": "22", "password": "pwkj123"}]}


def add_dynamic_host(self, hosts_list):
    for hosts in hosts_list:
        hostname = hosts.get("hostname")
        hostip = hosts.get("ip", hostname)
        hostport = hosts.get("hostport")
        password = hosts.get("password")
        my_host = Host(name=hostname, port=hostport)
        # self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_host', value=hostip)
        self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_pass', value=password)
        self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_port', value=hostport)
        self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_user', value=username)