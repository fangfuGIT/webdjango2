# -*- coding: utf-8 -*-

# Author： fangfu


import paramiko
from django.shortcuts import HttpResponse
from apps.models import ServerInfo
import pexpect
from apps.permissions.Decoding import encode_decode


class ssh_client(object):
    def ssh(id, command):
        ID = id
        line = ServerInfo.objects.get(id=ID)
        username = line.username
        pass_str = line.password
        password = encode_decode.decode(pass_str)
        port = line.port
        host = line.ipaddr

        if username:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(host, port, username, password, timeout=5)
                stdin, stdout, stderr = client.exec_command(command)
                result = stdout.read()
                client.close()
                return HttpResponse(result)
            except:
                return HttpResponse("Can not connect server, please check it !")
        else:
            return HttpResponse("Server id is not exist!")





class call_script(object):
    def test_script(id):
        ID = id
        line = ServerInfo.objects.get(id=ID)
        username = line.username
        pass_str = line.password
        password = encode_decode.decode(pass_str)
        port = line.port
        host = line.ipaddr
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, username, password, timeout=5)



        ss = pexpect.spawn('sh /root/test.sh')
        # ss.expect('password:')
        # ss.sendline('123456')
        #ss.expect(pexpect.EOF)
        return ss.before







# if __name__ == '__main__':
#     cmd = "df -h"
#     print(ssh(cmd))

