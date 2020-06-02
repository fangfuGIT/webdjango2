# -*- coding: utf-8 -*-

# Author： fangfu

import requests, json
from django.http import HttpResponse,HttpRequest
from apps import models


def received_sys_info(request):
    if request.method == 'GET':
        return HttpResponse("GET")

    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        id = received_json_data["id"]
        ipaddr = received_json_data["ipaddr"]
        cpu = received_json_data["cpu"]
        status = received_json_data["status"]
        models.CpuInfo.objects.create(received_json_data)

        # client = GetSysData.connect_db()
        # db = client[GetSysData.db]
        # collection = db[hostname]
        # collection.insert_one(received_json_data)
       # return HttpResponse(received_json_data)
        print(received_json_data)
        #return HttpResponse("Post successfully!")
    else:
        return HttpResponse("Have errors, Please Check your data!")