1、Python环境3.6+，编译安装 https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz



2、安装前需执行yum install mysql-devel gcc gcc-devel python-devel
   否则安装到mysqlclient会报错。

3、requirements.txt中没有写xadmin，因为直接安装会报错。xadmin需要单独安装，版本xadmin==2.0.1，需要先下载一个xadmin-django2.zip的包。
   安装命令：
   pip install --cache-dir . /root/xadmin-django2.zip（后面压缩包路径请自行更换）。
   也可以用这个命令来安装：
   pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2

4、 添加了bootstrap前端模板

5、 如果忘记后台密码
    python manage.py changepassword username
    创建超级用户
    python manage.py createsuperuser

    pip3 install psutil
    yum install -y libffi-devel python-devel openssl-devel