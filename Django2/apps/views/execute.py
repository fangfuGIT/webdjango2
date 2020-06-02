# -*- coding: utf-8 -*-

# Author： fangfu

from apps.models import ServerInfo, DataBaseInfo
from apps.permissions.Decoding import encode_decode
from apps.permissions.ansible_api import Runner
from django.http import JsonResponse, HttpResponse
from apps.permissions.paramiko import ssh_client, call_script
from apps import GetPendList
import os


def test(request):
    return HttpResponse("enforce.test")

class call_ansible(object):
    def call_command(request):
        id = request.POST.get('id')
        line = ServerInfo.objects.get(id=id)
        username = line.username
        pass_str = line.password
        password = encode_decode.decode(pass_str)
        port = line.port
        host = line.ipaddr
        args = request.POST.get('args')
        resource = {
            "webserver":
                [
                    {"hostname": host, "username": username, "hostport": port, "password": password}
                ]
        }

        rbt = Runner(resource)
        rbt.run_adhoc(cdhosts=host, module='shell', args=args)
        run_result = rbt.get_multi_result()
        return JsonResponse(run_result)

    def call_yml(request):
        resource = {
            "webserver":
                [
                    {"hostname": "183.61.123.33", "hostport": "22", "password": "pwkj123"},
                    {"hostname": "192.168.1.188", "hostport": "22", "password": "pwkj123"}
                ]
        }
        list = []
        for i in resource['webserver']:
            list.append(i["hostname"])

        for n in list:
            file = open('hosts', 'a')
            file.writelines([n, '\n'])
            file.close()

        rbt = Runner(resource)
        yml_path = "apps/permissions/ff.yml"
        rbt.run_playbook(yml_path=yml_path)
        result = rbt.get_multi_result()
       # os.remove('hosts')
        return JsonResponse(result)





    def call_init_yml(request):
        project = request.POST.get('project')
        servertype = request.POST.get('servertype')
        user = request.POST.get('user')
        password = request.POST.get('password')
        port = request.POST.get('port')
        time = request.POST.get('time')
        res = GetPendList.DataBaseView(time)

        if res:
            sys_init_list = [x[0].split(':')[0] for x in res]
        else:
            return HttpResponse("sys_init_list is empty, please check it!")
        resource = {"webserver": []}
        for num in sys_init_list:
            for k, v in resource.items():
                v.append({"hostname": num, "username": user, "hostport": port, "password": password})

        list = []
        for i in resource['webserver']:
            list.append(i["hostname"])
        mysqluser = 'root'
        mysqlpasswd = 'pwsgws.\#21'
        centrerConsoleIp = '192.168.1.189'

        file = open('hosts', 'a', encoding='UTF-8')
        for row in res:
            for n in row:
                file.write(str(n).lstrip('(b\'').rstrip('\',)') + '\t')
            file.write("mysqlUser="+mysqluser + '\t' + "mysqlPwd="+mysqlpasswd + '\t' + "centrerConsoleIp="+centrerConsoleIp + '\n')
        file.close()

        rbt = Runner(resource)
        yml_path = "apps/sysinit/sysinit.yml"
        rbt.run_playbook(yml_path=yml_path)
        result = rbt.get_multi_result()
        os.remove('hosts')
        return JsonResponse(result)


    def call_openarea(request):
        days = request.POST.get('days')
        GameProject = request.POST.get('GameProject')
        data_source = DataBaseInfo.objects.get(project=GameProject)
        user = data_source.username
        password = encode_decode.decode(data_source.password)
        port = data_source.port
        if days.isdigit():
            days = int(days) + 1
            host_ip = '192.168.1.188'
            db_port = 3306
            db_user = 'root'
            db_password = 'root'
            db_name = 'db_center_game'
            host_port = 22
            host_username = 'root'
            host_password = 'pwkj123'
            game_abbr = 'sgws'       # 以上这些参数是服务器相关权限，是需要从数据库里取，这里只是临时做测试的，后面要改。
            remote_path = '/tmp/model/'
            local_path = '/tmp/model/'   # remote_path和local_path如果是目录，一定要以'/'结尾；如果是文件则以文件名结尾。注意两个变量的格式必须一致。
            sql1 = "select distinct (case when b.idcid=1 then b.lanip else b.telecomip end) from t_product_server a ,t_server_fixedassets b where a.MasterDbId=b.id and a.plat<>'PW' and b.custommodel=2 and b.assetos=2 and OpenTime >date(now()) and OpenTime <adddate(DATE(NOW()),INTERVAL %s day) and status='3'" % days
            sql2 = "select concat('host','_',plat,'_',serverid,'_',(case when b.idcid=1 then b.lanip else b.telecomip end)) host, concat('ansible_ssh_host=',(case when b.idcid=1 then b.lanip else b.telecomip end)) sysip, concat('lanip=',b.lanip) lanip, concat('loginlanip=',(select (case when idcid=b.idcid then lanip else telecomip end) from t_server_fixedassets where a.serverip=TelecomIP)) loginlanip, concat('plat=',lower(Plat)) Plat, concat('serverid=',ServerId) ServerId  from  t_product_server a ,t_server_fixedassets b where a.MasterDbId=b.id and a.plat<>'PW' and b.custommodel=2 and b.assetos=2  and OpenTime >date(now()) and OpenTime <adddate(DATE(NOW()),INTERVAL %s day) and status=3 order by rand()" % (days)
            result1 = GetPendList.ExecuteSQL(host_ip, db_port, db_user, db_password, db_name, sql1)
            result2 = GetPendList.ExecuteSQL(host_ip, db_port, db_user, db_password, db_name, sql2)
            # sqldump1 = "mysqldump -u%s -p%s --skip-opt --set-gtid-purged=OFF --create-option -q -d -R -E --default-character-set=utf8 db_sgws_1001000 > db_sgws_model.sql" % (user, password)
            # sqldump2 = "mysqldump -u%s -p%s --skip-opt --set-gtid-purged=OFF --create-option -q -d -R -E --default-character-set=utf8 log_sgws_1001000 > db_log_model.sql" % (user, password)
            # sqldump3 = "mysqldump -u%s -p%s --skip-opt --set-gtid-purged=OFF --create-option -q -d -R -E --default-character-set=utf8 db_mart_1001000 > db_mart_model.sql" % (user, password)
            sqldump1 = "mysqldump -u%s -p%s db_%s_1001000 > %sdb_%s_model.sql" % (user, password, game_abbr, remote_path, game_abbr)
            sqldump2 = "mysqldump -u%s -p%s log_%s_1001000 > %sdb_log_model.sql" % (user, password, game_abbr, remote_path)
            sqldump3 = "mysqldump -u%s -p%s db_mart_1001000 > %sdb_mart_model.sql" % (user, password, remote_path)

            GetPendList.ExecuteShell(host_ip, host_port, host_username, host_password, sqldump1)
            GetPendList.ExecuteShell(host_ip, host_port, host_username, host_password, sqldump2)
            GetPendList.ExecuteShell(host_ip, host_port, host_username, host_password, sqldump3)
            GetPendList.RemoteScp(host_ip, host_port, host_username, host_password, remote_path, local_path)
            #return HttpResponse('all done')

            if result1:
                file = open('waitproc_list', 'a', encoding='UTF-8')
                openarea_list = [x[0] for x in result1]
                file.write('[copyfile]' + '\n')
                file.write(str(openarea_list[0]) + '\n')
                if result2:
                    file.write('[open]' + '\n')
                    for x in result2:
                        for n in x:
                            file.write(str(n).lstrip('(b\'').rstrip('\',)') + '\t')
                        file.write('\n')
                file.close()
            else:
                return HttpResponse("No query in the OpenArea List, Please try again!")
        else:
            return HttpResponse("The days must be a Positive integer, Please input a Positive integer!")

        resource = {"webserver": []}
        for num in result2:
            for k, v in resource.items():
                v.append({"hostname": num, "username": user, "hostport": port, "password": password})
        list = []
        for i in resource['webserver']:
            list.append(i["hostname"])
        mysqlUser = 'root'
        mysqlPwd = 'pwsgws.#21'
        centrerConsoleIp = '192.168.1.189'
        file = open('hosts', 'a', encoding='UTF-8')
        for row in result2:
            for n in row:
                file.write(str(n).lstrip('(b\'').rstrip('\',)') + '\t')
            file.write("mysqlUser=" + mysqlUser + '\t' + "mysqlPwd=" + mysqlPwd + '\t')
            file.write('\n')
        file.close()
        return HttpResponse(resource)


class call_shell(object):
    def ssh_server(request):
        id = request.POST.get('id')
        command = request.POST.get('command')
        return ssh_client.ssh(id, command)

    def call_script(request):
        id = request.POST.get('id')
        return call_script.test_script(id)