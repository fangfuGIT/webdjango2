# -*- coding: utf-8 -*-

# Author： fangfu


import psutil




def sys_cpu():
    #cpu_core = psutil.cpu_count()
    cpu_core = psutil.cpu_count(logical=False)  #CPU内核数量
    #arg = psutil.cpu_times()

    sys_cpu = {}
    cpu_time = psutil.cpu_times_percent(interval=1)

    sys_cpu['percent'] = psutil.cpu_percent(interval=1)  #CPU总使用率
    sys_cpu['lcpu_percent'] = psutil.cpu_percent(interval=1, percpu=True) #各个CPU的使用率

    sys_cpu['user'] = cpu_time.user
    sys_cpu['nice'] = cpu_time.nice
    sys_cpu['system'] = cpu_time.system
    sys_cpu['idle'] = cpu_time.idle

    loadavg = psutil.getloadavg() # cpu平均负载,返回最近1、5、15分钟内的平均负载

    print(cpu_time)
    print(cpu_core)
    print(loadavg)



def sys_mem():
    mem = {}
    virtual_memory = psutil.virtual_memory()
    mem['total'] = virtual_memory.total
    mem['available'] = virtual_memory.available
    mem['percent'] = virtual_memory.percent
    mem['used'] = virtual_memory.used
    mem['free'] = virtual_memory.free

    print(virtual_memory)
    print(mem)


def sys_disk():
    disk = {}
    disk_partitions = psutil.disk_partitions()
    disk_usage = psutil.disk_usage('/')
    disk_io_counters = psutil.disk_io_counters()

    print(disk_partitions)
    print(disk_usage)
    print(disk_io_counters)


def sys_net():
    net_io_counters = psutil.net_io_counters()
    #net_io_counters = psutil.net_io_counters(pernic=True)
    net_connections = psutil.net_connections()
    net_if_addrs = psutil.net_if_addrs()
   # process_connections = psutil.Process.connections()


    print(net_io_counters)
    print(net_connections)
    print(net_if_addrs)


def sys_pids():
    pid = 74
    all_pids = psutil.pids()
    pro = psutil.Process(pid)
    #pro.cwd()


    #print(all_pids)
    print(pro.cwd())

if __name__ == "__main__":
    #sys_cpu()
    #sys_mem()
    #sys_disk()
    #sys_net()
    sys_pids()