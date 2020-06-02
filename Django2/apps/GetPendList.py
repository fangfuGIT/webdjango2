# # _*_ coding: utf-8 _*_
# __author__ = 'fangfu'
# __date__ = '2018/8/25 16:33'

import MySQLdb
import paramiko


def DataBaseView(time):
    #conn = MySQLdb.connect(host='192.168.1.215', port=2433, user='dbwrit', passwd='writ$#@', db='db_center_game')
    conn = MySQLdb.connect(host='192.168.1.188', port=3306, user='root', passwd='root', db='db_center_game')
    cursor = conn.cursor()
    #sql = "select concat((case when a.idcid=1 then a.lanip else a.telecomip end ),':22') telecomip ,concat('lanip=',lanip) lanip,concat('CustomModel=',CustomModel)  CustomModel ,concat('systype=m')  systype,concat('m_slanip=',(select lanip from t_server_fixedassets k where k.id=b.SlaveDBId)) m_slanip from t_server_fixedassets a inner join t_server_dblist b on a.id=b.masterdbid where  a.RecordDate >'2017-12-04 17:35:15' and a.CustomModel in (2,3) and  a.idcid <>1 union all select concat((case when a.idcid=1 then a.lanip  else a.telecomip end ),':22') telecomip ,concat('lanip=',lanip) lanip,concat('CustomModel=',CustomModel)  CustomModel ,concat('systype=s')  systype,concat('m_slanip=',(select lanip from t_server_fixedassets k where k.id=b.masterDBId)) m_slanip from t_server_fixedassets a inner join t_server_dblist b on a.id=b.slavedbid where  a.RecordDate >'2017-12-04 17:35:15' and a.CustomModel in (2,3) and  a.idcid <>1"
    #sql = "select serverIp,PlatId,serverid from t_product_server where plat = 'QQ'"
    #sql = "select ipaddr from apps_serverinfo"

    sql1 = "select concat((case when a.idcid=1 then a.lanip  else a.telecomip end ),':22') telecomip,concat('lanip=',lanip) lanip,concat('CustomModel=',CustomModel)  CustomModel ,concat('systype=m')  systype,concat('m_slanip=',(select lanip from t_server_fixedassets k where k.id=b.SlaveDBId)) m_slanip from t_server_fixedassets a inner join t_server_dblist b on a.id=b.masterdbid where a.RecordDate>%s and a.CustomModel in (2,3) and  a.idcid <>1 union all select concat((case when a.idcid=1 then a.lanip  else a.telecomip end ),':22') telecomip,concat('lanip=',lanip) lanip,concat('CustomModel=',CustomModel)  CustomModel ,concat('systype=s')  systype,concat('m_slanip=',(select lanip from t_server_fixedassets k where k.id=b.masterDBId)) m_slanip from t_server_fixedassets a inner join t_server_dblist b on a.id=b.slavedbid where a.RecordDate>%s and a.CustomModel in (2,3) and  a.idcid <>1"
    cursor.execute(sql1 % (time, time))
    # sql = "select concat((case when a.idcid=1 then a.lanip  else a.telecomip end ),':22') telecomip from t_server_fixedassets a where telecomip = '192.168.2.236'"
    #cursor.execute(sql)
    rs = cursor.fetchall()
    sql2 = ""
    return rs


def ExecuteSQL(db_host, db_port, db_user, db_password, db_name, sql):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_name)
    cursor = conn.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()
    return rs


def ExecuteShell(host_ip, host_port, host_username, host_password, shell):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host_ip, host_port, host_username, host_password)
    stdin, stdout, stderr = ssh.exec_command(shell)
    return stdout.read()


def RemoteScp(host_ip, host_port, host_username, host_password, remote_path, local_path):
    scp = paramiko.Transport((host_ip, host_port))
    scp.connect(username=host_username, password=host_password)
    sftp = paramiko.SFTPClient.from_transport(scp)
    try:
        remote_files = sftp.listdir(remote_path)
        for file in remote_files:
            local_file = local_path + file
            remote_file = remote_path + file
            sftp.get(remote_file, local_file)
    except IOError:
        return ("remote_path or local_path is not exist!")
    scp.close()


def call_good_yml(request):
    user = request.POST.get('user')
    password = request.POST.get('passwd')
    port = request.POST.get('port')

    res = DataBaseView()
    list = [x[0] for x in res]
    print(list)
    resource = {
        "webserver":
            [
                {"hostname": "", "username": user, "hostport": port, "password": password},
            ]
    }
    for num in list:
        for k, v in resource.items():
            v.append({"hostname": num})
    return resource


def database_mysqldump():
    root = 'root'
    password = 'password'
    conn = MySQLdb.connect(host='192.168.1.188', port=3306, user='root', passwd='root')
    cursor = conn.cursor()
    sql1 = "mysqldump -uroot -p --skip-opt --set-gtid-purged=OFF --create-option -q -d -R -E --default-character-set=utf8 db_sgws_1001000 > db_sgws_model.sql"
    "mysqldump -uroot -p --skip-opt --set-gtid-purged=OFF --create-option -q -d -R -E --default-character-set=utf8 log_sgws_1001000 > db_log_model.sql"
    "mysqldump -uroot -p --skip-opt --set-gtid-purged=OFF --create-option -q -d -R -E --default-character-set=utf8 db_mart_1001000 > db_mart_model.sql"
    cursor.execute(sql1)
    rs = cursor.fetchall()
    return rs
    pass