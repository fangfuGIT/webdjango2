# -*- coding: utf-8 -*-

# Author： fangfu


import requests, json
import psutil






def test():
    user = "fangfu"
    passwd = '123..com'

    server_ip = "127.0.0.1:8000"
    sys_info = {
	    "id": 3,
            "ipaddr": "2.2.2.2",
            "cpu": 2,
            "status": "2",
	    "owner": 1
        }
    idc_info = {
            "id": 3,
            "name": "333",
            "position": 333,
            "status": "3",
            "owner": "fangfu"
        }

    json_data = json.dumps(sys_info)
    idc_data = json.dumps(idc_info)
    print(json_data)
    url = 'http://{0}/idc/'.format(server_ip)
    head = {"Content-Type": "application/json; charset=UTF-8"}
    print(url)

    #result = requests.post(url, data=json_data, auth=(user, passwd))
    get_result = requests.get("http://127.0.0.1:8000/cpu")
    #result = requests.post("http://127.0.0.1:8000/cpu/", data=json_data, headers=head, auth=(user, passwd))
    result = requests.post("http://127.0.0.1:8000/idc/", data=idc_data, headers=head, auth=(user, passwd))
    #result = requests.post("http://127.0.0.1:8000/cpu/", data=json_data, headers=head)

    print(result)
    print(get_result.text)
    # post_data("http://{0}/cpu/".format(server_ip), json_data)

    if result.status_code == 200:
        print('success')
    else:
        print(result.status_code)



def ppp():
    cpu_core = psutil.cpu_count()
    #arg = psutil.cpu_count(logical=False)
    #arg = psutil.cpu_times()

    # sys_cpu = {}
    # cpu_time = psutil.cpu_times_percent(interval=1)
    # sys_cpu['percent'] = psutil.cpu_percent(interval=1)
    # sys_cpu['lcpu_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    # sys_cpu['user'] = cpu_time.user
    # sys_cpu['nice'] = cpu_time.nice
    # sys_cpu['system'] = cpu_time.system
    # sys_cpu['idle'] = cpu_time.idle


    #print(sys_cpu)

    server_ip = "127.0.0.1:8000"
    sys_info = {
        #"id": 3,
        "ipaddr": "127.0.0.1",
        "cpu": cpu_core,
        "status": "2",
        "owner": 1
    }
    json_data = json.dumps(sys_info)
    head = {"Content-Type": "application/json; charset=UTF-8"}
    result = requests.post("http://127.0.0.1:8000/cpu/", data=json_data, headers=head)
    print(result.text)

    print(cpu_core)

if __name__ == "__main__":
    #test()
    ppp()