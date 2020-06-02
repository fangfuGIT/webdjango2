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


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_failed = {}
        self.host_unreachable = {}
    def v2_runner_on_ok(self, result, *args, **kwargs):
        host = result._host.get_name()
        self.runner_on_ok(host, result._result)
        self.host_ok[host] = result
    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result)
        self.host_ok[host] = result
    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        self.host_ok[host] = result


# class PlaybookCallback(CallbackBase):
#     def __init__(self, *args, **kwargs):
#         #super(PlaybookCallback, *args).__init__(self, *args, **kwargs)
#         self.task_ok = {}
#         self.task_failed = {}
#         self.task_unreachable = {}
#         self.task_stats = {}
#         self.task_skipped = {}
#     def v2_runner_on_ok(self, result, *args, **kwargs):
#         self.task_ok[result._host.get_name()] = result
#     def v2_runner_on_failed(self, result, *args, **kwargs):
#         self.task_failed[result._host.get_name()] = result
#     def v2_runner_on_unreachable(self, result):
#         self.task_unreachable[result._host.get_name()] = result


class Runner(object):
    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.results_raw = {}
        self.__initializeData()
        #self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def __initializeData(self):
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff', 'listhosts', 'listtasks', 'listtags', 'syntax']
                             )
        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=10, become=None, become_method=None, become_user=None, check=False, diff=False, listhosts=False, listtasks=False, listtags=False, syntax=False)
        self.inventory = InventoryManager(loader=self.loader, sources='hosts')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        for k, v in self.resource.items():
            self.add_dynamic_host(v)

    def add_dynamic_host(self, hosts_list):
        for hosts in hosts_list:
            hostname = hosts.get("hostname")
            hostport = hosts.get("hostport")
            password = hosts.get("password")
            username = hosts.get("username")
            my_host = Host(name=hostname, port=hostport)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_host', value=hostname)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_pass', value=password)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_port', value=hostport)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_user', value=username)
            self.inventory.add_host(host=hostname, port=hostport)

    def run_adhoc(self, cdhosts, module, args):
        play_source = dict(
            name="Ansible Play",
            hosts=cdhosts,
            gather_facts='no',
            tasks=[
                dict(action=dict(module=module, args=args))
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        #self.passwords = dict(vault_pass='xxx')
        # if extra_vars:
        #     self.variable_manager.extra_vars = extra_vars
        self.callback = ResultCallback()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, yml_path):
        #if extra_vars:
        #    self.variable_manager.extra_vars = extra_vars
        playbook = PlaybookExecutor(
            playbooks=[yml_path],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
        )
        self.callback = ResultCallback()
        playbook._tqm._stdout_callback = self.callback
        playbook.run()

    def get_alone_result(self):
        self.result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.result_raw['success'][host] = result._result
            if 'stdout' in self.result_raw['success'][host]:
                return json.dumps(self.result_raw['success'][host]['stdout'])
            else:
                return json.dumps(self.result_raw['success'][host])
        for host, result in self.callback.host_failed.items():
            self.result_raw['failed'][host] = result._result
            return json.dumps(self.result_raw['failed'])
        for host, result in self.callback.host_unreachable.items():
            self.result_raw['unreachable'][host] = result._result
            return json.dumps(self.result_raw['unreachable'])

    def get_multi_result(self):
        self.result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.result_raw['success'][host] = result._result
        for host, result in self.callback.host_failed.items():
            self.result_raw['failed'][host] = result._result
        for host, result in self.callback.host_unreachable.items():
            self.result_raw['unreachable'][host] = result._result
        return self.result_raw



if __name__ == '__main__':
    resource = {
        "webserver":
                [
                {"hostname": "192.168.2.234", "username": "root", "hostport": "22", "password": "pwkj123"},
                {"hostname": "192.168.2.236", "username": "root", "hostport": "22", "password": "pwkj123"}
                ]
    }
    rbt = Runner(resource)


    # rbt.run_adhoc(cdhosts=["192.168.2.234"], module='shell', args='ifconfig')

    # run_result = rbt.get_alone_result()
    # print(run_result)

    # run_result = rbt.get_multi_result()
    # print(run_result)

   # rbt = Runner(['192.168.2.234'], ['ff.yml'])

    #------------------------------------------------------------------

    #rbt.run_playbook(yml_path='ff.yml', extra_vars={"user": "root"})
    rbt.run_playbook(yml_path='ff.yml')
    run_result = rbt.get_multi_result()
    print(run_result)



