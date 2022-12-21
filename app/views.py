# coding=utf-8
__author__ = 'fanghouguo'

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

import Query
import UserTime
import json
import time
from model.newworkingmodel import networkingmodel
from model.rackmodel import rackmodel
from model.roommodel import roommodel
from model.servermodel import servermodel
from model.servicemodel import servicemodel
from model.usermodel import usermodel
from model.vmmodel import vmmodel


# dashbord page
@login_required
def index(request):
    rm = roommodel()
    rc = rackmodel()
    sv = servermodel()
    v = vmmodel()
    room_num = rm.count({})
    rack_num = rc.count({})
    server_num = sv.count({})
    vm_num = v.count({})
    online_num = sv.count({"status": 1})
    offline_num = server_num - sv.count({"status": 1})
    return render(request, 'index.html',
                  {"room": room_num, 'rack': rack_num, 'server': server_num, 'vm': vm_num, 'online': online_num,
                   'offline': offline_num})


@login_required
def deleteRackById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        rk = rackmodel()
        ret = rk.delete({"id": id})
        if ret:
            result = {"ret": "delete success"}

    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def getRackById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")

    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']

    idc = rackmodel()

    r = idc.find({"id": id})

    result = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'service_provider_name']

    srv = servicemodel()

    r_1 = srv.find({})
    servers = Query.fSqlResult(r_1, key_list_1)

    ret = {'result': result[0], 'sel': servers}

    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
@csrf_protect
def ajax_rack_list(request):
    page = request.REQUEST.get('p', 1)

    pageSize = request.REQUEST.get('pageSize', 6)

    # conn = SqlConn()

    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']

    rk = rackmodel()

    r = rk.find({})

    result = Query.fSqlResult(r, key_list)

    totalPage = rk.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    key_list_1 = ['id', 'service_provider_name']

    svr = servicemodel()

    r_1 = svr.find({})

    servers = Query.fSqlResult(r_1, key_list_1)

    new_service = {}

    for srv in servers:
        for id in srv:
            print
            id
            if id == 'id':
                new_service[srv[id]] = srv['service_provider_name']

    new_result = []
    for item in result:
        if new_service.has_key(item['service_provider']):
            item['service_provider'] = new_service[item['service_provider']]
        item['start_time'] = UserTime.utcToString(float(item['start_time']))
        item['end_time'] = UserTime.utcToString(float(item['end_time']))
        new_result.append(item)

    head = {'a_id': "自增序号", 'b_idc_name': "机柜名称", 'c_rack_number': "机柜编号", 'd_start_time': "开始时间", 'e_end_time': "结束时间",
            'f_service_provider': "服务提供商", "x_oper": "操作"}

    ret = {
        "body": result,
        "head": head,
        "page": {
            "current": page,
            "totalpage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


@login_required
@csrf_protect
def rack_jgt(request):
    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']
    rk = rackmodel()
    r = rk.find({})
    result = Query.fSqlResult(r, key_list)
    key_list_1 = ['id', 'hostname', 'manage_ip', 'other_ip', 'app_name', 'cpu', 'mem', 'disk', 'sn', 'an', 'units',
                  'idc_name', 'rack_number', 'rack_units', 'status', 'system_version']
    new_result = []
    for srv in result:
        sv = servermodel()
        r_1 = sv.find({"idc_name": srv['id']})
        servers = Query.fSqlResult(r_1, key_list_1)
        idc_name = srv['idc_name']
        new_result.append([idc_name, servers])

    return render(request, 'rack/rack_demo.html',
                  {'ret': new_result, "menu": "submenu1"})


@login_required
@csrf_protect
def rack_list(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)

    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']

    rk = rackmodel()
    r = rk.find({})
    result = Query.fSqlResult(r, key_list)

    totalPage = rk.count({})

    print
    "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    key_list_1 = ['id', 'service_provider_name']
    svr = servicemodel()
    r_1 = svr.find({})
    servers = Query.fSqlResult(r_1, key_list_1)

    new_service = {}
    for srv in servers:
        for id in srv:
            print
            id
            if id == 'id':
                new_service[srv[id]] = srv['service_provider_name']

    new_result = []
    for item in result:
        if new_service.has_key(item['service_provider']):
            item['service_provider'] = new_service[item['service_provider']]
        item['start_time'] = UserTime.utcToString(float(item['start_time']))
        item['end_time'] = UserTime.utcToString(float(item['end_time']))
        new_result.append(item)

    return render(request, 'rack/rack_list.html',
                  {'ret': result, 'totalpage': totalPage, 'current': page, 'lastPage': totalPage})


@login_required
@csrf_protect
def new_rack(request):
    name_tips = ""
    insert = {}
    if request.method == 'POST':
        idc_name = request.REQUEST.get('idc_name')
        rack_number = request.REQUEST.get('rack_number')
        start_time = request.REQUEST.get('start_time')
        end_time = request.REQUEST.get('end_time')
        service_provider = request.REQUEST.get('service_provider')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))
        print
        idc_name, rack_number, start_time, end_time, service_provider
        print
        "editor=" + str(editor), "id=" + str(id)
        table = 'idc'
        isF = isexist(table, 'idc_name', idc_name)
        insert = {"idc_name": idc_name, 'rack_number': rack_number, 'start_time': UserTime.stringToUtc(start_time),
                  'end_time': UserTime.stringToUtc(end_time),
                  'service_provider': service_provider}
        if isF == 1 and editor == 0:
            name_tips = "名称重复"
        elif idc_name is not None and rack_number is not None:
            start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_time = time.mktime(start_time)
            end_time = time.mktime(end_time)
            if start_time > end_time:
                return

            sql = ""
            rk = rackmodel()
            if editor and id:
                # sql = Sql.get_u_sql(table, insert, {"id": id})
                rack_id = rk.update(insert, {"id": id})
            else:
                # sql = Sql.get_i_sql(table, insert)
                rack_id = rk.insert(insert)

            if rack_id:
                return HttpResponseRedirect("/rack_list/?p=" + str(editor_current_page))
        else:
            name_tips = "参数错误"

    key_list = ['id', 'service_provider_name']
    svr = servicemodel()
    r = svr.find({})
    result = Query.fSqlResult(r, key_list)
    return render(request, 'rack/new_rack.html',
                  {'service_provider_list': result, "val": insert, "name_tips": name_tips})


@login_required
def rack_config(request):
    return render(request, 'rack/new_rack_config.html', {})


@login_required
def new_rack_config(request):
    if request.method == 'POST':
        idc_name = request.REQUEST.get('idc_name')
        rack_number = request.REQUEST.get('rack_number')
        start_time = request.REQUEST.get('start_time')
        end_time = request.REQUEST.get('end_time')
        service_provider = request.REQUEST.get('service_provider')
        print
        idc_name, rack_number, start_time, end_time, service_provider
        if idc_name is not None and rack_number is not None:
            start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_time = time.mktime(start_time)
            end_time = time.mktime(end_time)
            if start_time > end_time:
                return

            insert = {"idc_name": idc_name, 'rack_number': rack_number, 'start_time': start_time, 'end_time': end_time,
                      'service_provider': service_provider}
            table = 'idc'
            rk = rackmodel()
            rack_id = rk.insert(insert)

            if rack_id:
                return HttpResponseRedirect("/rack_list/")
    else:
        pass

    key_list = ['id', 'room_name']
    rm = roommodel()
    r = rm.find({})
    result = Query.fSqlResult(r, key_list)
    key_list_1 = ['id', 'idc_name']

    # sql_1 = Sql.get_s_sql('idc', key_list_1, {})

    rk = rackmodel()
    r_1 = rk.find({})
    result_1 = Query.fSqlResult(r_1, key_list_1)
    return render(request, 'new__config.html', {'room_list': result, 'rack_list': result_1})


# is field isexist
def isexist(md, key, val):
    key_list = ['id']
    r = md.find({key: val})
    result = Query.fSqlResult(r, key_list)
    if result:
        return 1
    return 0


@login_required
def network_config(request):
    key_list = ['id', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units', 'rack_number',
                'rack_units']

    rk = rackmodel()
    r = rk.find({})
    result = Query.fSqlResult(r, key_list)

    return render(request, 'network/network_config.html', {'ret': result})


@login_required
@csrf_protect
def new_network_config(request):
    name_tips = ""
    insert = {}
    if request.method == 'POST':
        device_name = request.REQUEST.get('device_name')
        idc_name = request.REQUEST.get('idc_name')
        manage_ip = request.REQUEST.get('manage_ip')
        other_ip = request.REQUEST.get('other_ip')
        dev_type = request.REQUEST.get('dev_type')
        dev_ports = request.REQUEST.get('dev_ports')
        sn = request.REQUEST.get('sn')
        an = request.REQUEST.get('an')
        units = request.REQUEST.get('units')
        rack_number = request.REQUEST.get('rack_number')
        rack_units = request.REQUEST.get('rack_units')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))

        insert = {
            'device_name': device_name,
            "idc_name": idc_name,
            'manage_ip': manage_ip,
            'other_ip': other_ip,
            'dev_type': dev_type,
            'dev_ports': dev_ports,
            'sn': sn,
            'an': an,
            'units': units,
            'rack_number': rack_number,
            'rack_units': rack_units
        }

        table = 'network_config'
        nw = networkingmodel()
        isF = isexist(nw, 'device_name', device_name)
        if isF == 1 and editor == 0:
            name_tips = "名称重复"
        elif idc_name is not None and rack_number is not None:
            if editor and id:
                rack_id = nw.update(insert, {"id": id})
            else:

                rack_id = nw.insert(insert)

            if rack_id:
                return HttpResponseRedirect("/network_config/?p" + str(editor_current_page))
        else:
            name_tips = "参数错误"

    rm = roommodel()
    key_list = ['id', 'room_name']
    r = rm.find({})
    result = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    rk = rackmodel()
    r_1 = rk.find({})
    result_1 = Query.fSqlResult(r_1, key_list_1)
    return render(request, 'network/new_network_config.html',
                  {'room_list': result, 'rack_list': result_1, "name_tips": name_tips, "val": insert})


@login_required
def getNetwork_configById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")

    key_list = ['id', 'device_name', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units',
                'rack_number',
                'rack_units']
    # sql = Sql.get_s_sql('network_config', key_list, {"id": id})
    nw = networkingmodel()
    r = nw.find({"id": id})
    result = Query.fSqlResult(r, key_list)

    key_list = ['id', 'room_name']
    # sql = Sql.get_s_sql('room', key_list, {})
    rm = roommodel()
    r = rm.find({})
    room = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    # sql_1 = Sql.get_s_sql('idc', key_list_1, {})
    rk = rackmodel()
    r_1 = rk.find({})
    idc = Query.fSqlResult(r_1, key_list_1)

    ret = {'result': result[0], 'idc': idc, 'room': room}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def deleteNetwork_configById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:

        # sql = Sql.get_d_sql('network_config', {"id": id})
        nw = networkingmodel()
        r = nw.delete({"id": id})
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def ajax_network_config(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)

    key_list = ['id', 'device_name', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units',
                'rack_number',
                'rack_units']

    nw = networkingmodel()
    r = nw.find({})
    result = Query.fSqlResult(r, key_list)

    totalPage = nw.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    key_list = ['id', 'room_name']
    # sql = Sql.get_s_sql('room', key_list, {})
    rm = roommodel()
    r = rm.find({})
    room = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    # sql_1 = Sql.get_s_sql('idc', key_list_1, {})
    rk = rackmodel()
    r_1 = rk.find({})
    idc = Query.fSqlResult(r_1, key_list_1)

    head = {
        'a_id': "自增序号",
        'b_device_name': "设备名称",
        'c_idc_name': "所在机房",
        'd_manage_ip': "管理IP",
        'e_other_ip': "非管理IP",
        'j_rack_number': "所在机柜",
        'k_rack_units': "机柜编号",
        "x_oper": "操作"
    }
    new_room = {}
    for j in room:
        new_room[j['id']] = j['room_name']
    new_idc = {}
    for k in idc:
        new_idc[k['id']] = k['idc_name']
    new_result = []
    for item in result:
        if new_room.has_key(item['idc_name']):
            item['idc_name'] = new_room[item['idc_name']]
        if new_idc.has_key(item['rack_number']):
            item['rack_number'] = new_idc[item['rack_number']]
        new_result.append(item)
    ret = {
        "body": new_result,
        "head": head,
        "idc": idc,
        'room': room,
        "page": {
            "current": page,
            "totalpage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


@login_required
def getServerById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")

    key_list = ['id',
                'hostname',
                'manage_ip',
                'other_ip',
                'app_name',
                'system_version',
                'zabbix_template',
                'owner_group',
                'server_type',
                'cpu',
                'mem',
                'disk',
                'sn',
                'an',
                'units',
                'idc_name',
                'rack_number',
                'rack_units',
                'create_date',
                'end_date',
                'switch_name',
                'switch_port',
                'change_time',
                'change_dev_info',
                'change_people',
                'description',
                'status'
                ]
    # sql = Sql.get_s_sql('server', key_list, {"id": id})
    sv = servermodel()
    r = sv.find({"id": id})
    result = Query.fSqlResult(r, key_list)

    key_list = ['id', 'room_name']
    # sql = Sql.get_s_sql('room', key_list, {})
    rm = roommodel()
    r = rm.find({})
    room = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    # sql_1 = Sql.get_s_sql('idc', key_list_1, {})
    rk = rackmodel()
    r = rk.find({})
    idc = Query.fSqlResult(r_1, key_list_1)

    key_list_2 = ['id', 'device_name']
    # sql_2 = Sql.get_s_sql('network_config', key_list_2, {})
    nw = networkingmodel()
    r_2 = nw.find({})
    network = Query.fSqlResult(r_2, key_list_2)

    ret = {'result': result[0], 'idc': idc, 'room': room, 'owner_group': ServerGroup.group,
           'server_type': ServerGroup.type, 'network': network}
    print
    "ret=" + str(ret)
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def deleteServerById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:

        # sql = Sql.get_d_sql('server', {"id": id})
        sv = servermodel()
        r = sv.delete({"id": id})
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required()
def server(request):
    key_list = ['id', 'hostname', 'manage_ip', 'other_ip', 'app_name', 'cpu', 'mem', 'disk', 'sn', 'an', 'units',
                'idc_name', 'rack_number', 'rack_units', 'status']
    # sql = Sql.get_s_sql('server', key_list, {})
    sv = servermodel()
    r = sv.find({})
    result = Query.fSqlResult(r, key_list)

    head = ['id', 'host name', 'manager ip', 'other IP', 'app nane', 'CPU', 'memory', 'disk', 'sn', 'an', 'units',
            'room', 'rack', 'rack number', 'status', 'oper']
    return render(request, 'server/server.html', {'ret': result, 'data': result, 'head': head, 'body': result})


@login_required
def ajaxserver(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    sv = servermodel()
    key_list = [
        'id',
        'hostname',
        'manage_ip',
        'other_ip',
        'app_name',
        'cpu', 'mem', 'disk', 'sn', 'an', 'units',
        'idc_name', 'rack_number', 'rack_units', 'status']

    r = sv.find({})
    result = Query.fSqlResult(r, key_list)

    rk = rackmodel()
    totalPage = rk.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    head = {
        'a_id': " 自增序号",
        'b_hostname': "主机名称",
        'c_manage_ip': "管理IP",
        'd_other_ip': "非管理IP",
        'f_cpu': "CPU",
        'g_mem': "内存",
        'h_disk': "硬盘",
        'o_status': "状态",
        'p_oper': "操作"
    }

    ret = {
        "body": result,
        "head": head,
        "page": {
            "current": page,
            "totalPage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


@login_required
@csrf_protect
def new_server(request):
    name_tips = ""
    insert = {}
    if request.method == 'POST':
        idc_name = request.REQUEST.get('idc_name')
        hostname = request.REQUEST.get('hostname')
        manage_ip = request.REQUEST.get('manage_ip')
        other_ip = request.REQUEST.get('other_ip')
        app_name = request.REQUEST.get('app_name')
        system_version = request.REQUEST.get('system_version')
        zabbix_template = request.REQUEST.get('zabbix_template')
        owner_group = request.REQUEST.get('owner_group')
        server_type = request.REQUEST.get('server_type')
        cpu = request.REQUEST.get('cpu')
        mem = request.REQUEST.get('mem')
        disk = request.REQUEST.get('disk')
        sn = request.REQUEST.get('sn')
        an = request.REQUEST.get('an')
        units = request.REQUEST.get('units')
        rack_number = request.REQUEST.get('rack_number')
        rack_units = request.REQUEST.get('rack_units')
        create_date = request.REQUEST.get('create_date')
        end_date = request.REQUEST.get('end_date')
        switch_name = request.REQUEST.get('switch_name')
        switch_port = request.REQUEST.get('switch_port')
        # change_time = request.REQUEST.get('change_time',None)
        change_dev_info = request.REQUEST.get('change_dev_info', None)
        change_people = request.REQUEST.get('change_people', None)
        description = request.REQUEST.get('description')
        status = request.REQUEST.get('status')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))

        sv = servermodel()

        insert = {
            "hostname": hostname,
            'manage_ip': manage_ip,
            'other_ip': other_ip,
            'app_name': app_name,
            'system_version': system_version,
            'zabbix_template': zabbix_template,
            'owner_group': owner_group,
            'server_type': server_type,
            'cpu': cpu,
            'mem': mem,
            'disk': disk,
            'sn': sn,
            'an': an,
            'units': units,
            'rack_number': rack_number,
            'rack_units': rack_units,
            'create_date': create_date,
            'end_date': end_date,
            'switch_name': switch_name,
            'switch_port': switch_port,
            'description': description,
            'status': status,
            'idc_name': idc_name
        }
        table = 'server'
        isF = isexist(table, 'hostname', hostname)
        if isF == 1 and editor == 0:
            name_tips = "名称重复"
        elif hostname and manage_ip:
            if editor and id:
                insert['change_time'] = time.time()
            if change_dev_info:
                insert['change_dev_info'] = change_dev_info
            if change_people:
                insert['change_people'] = change_people

            if editor and id:
                afeck_row = sv.update(insert, {"id": id})
            else:
                afeck_row = sv.insert(insert)

            if afeck_row:
                return HttpResponseRedirect("/server/?p=" + str(editor_current_page))
        else:
            name_tips = "参数错误"

    key_list = ['id', 'room_name']
    # sql = Sql.get_s_sql('room', key_list, {})
    rm = roommodel()
    r = rm.find({})
    result = Query.fSqlResult(r, key_list)
    key_list_1 = ['id', 'idc_name']

    # sql_1 = Sql.get_s_sql('idc', key_list_1, {})
    rk = rackmodel()
    r_1 = rk.find({})
    result_1 = Query.fSqlResult(r_1, key_list_1)

    server_group = ServerGroup.group
    server_type = ServerGroup.type
    key_list_2 = ['id', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units',
                  'rack_number',
                  'rack_units']
    # sql_2 = Sql.get_s_sql('network_config', key_list_2, {})
    nw = networkingmodel()

    r_2 = nw.find({})

    result_2 = Query.fSqlResult(r_2, key_list_2)

    return render(request, 'server/new_server.html',
                  {'server_group': server_group, 'server_type': server_type, 'room_list': result, 'rack_list': result_1,
                   'network': result_2, "val": insert, "name_tips": name_tips})


########################################## server end

@login_required
def statistics(request):
    return render(request, 'statistics.html', {})


@login_required
def users(request):
    key_list = ['id', 'username', 'is_active', 'date_joined', 'email', 'last_login']
    u = usermodel()
    r = u.find({})
    result = Query.fSqlResult(r, key_list)
    return render(request, 'users/users.html', {'ret': result})


@login_required
@csrf_protect
def ajax_users(request):
    page = request.REQUEST.get('p', 1)

    pageSize = request.REQUEST.get('pageSize', 6)

    key_list = ['id', 'username', 'is_active', 'date_joined', 'email', 'last_login']

    u = usermodel()

    r = u.find({})

    result = Query.fSqlResult(r, key_list)

    totalPage = u.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    head = {'a_id': "用户ID", 'b_username': "用户名称", 'c_is_active': "是否可用", 'd_date_joined': "加入时间", 'e_email': "邮件",
            'f_last_login': "最后登录"}
    new_result = []

    for i in result:
        if i['is_active']:
            i['is_active'] = '可用'
        if i['date_joined']:
            i['date_joined'] = str(i['date_joined'])
        if i['last_login']:
            i['last_login'] = str(i['last_login'])
        new_result.append(i)
    print
    new_result
    ret = {
        "body": new_result,
        "head": head,
        "page": {
            "current": page,
            "totalpage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


@login_required
def deleteUsersById(request):
    id = request.REQUEST.get('id', None)
    result = {"ret": "delete faild"}
    if id:
        u = usermodel()
        r = u.delete({"id": id})
        result = {"ret": "delete success"}

    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def getUsersById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")

    key_list = ['id', 'username', 'is_active', 'date_joined', 'email', 'last_login']

    u = usermodel()
    r = u.find({"id": id})
    result = Query.fSqlResult(r, key_list)
    ret = {'result': result[0]}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@csrf_protect
def new_users(request):
    if request.method == 'POST':
        user_name = request.REQUEST.get('user_name')
        user_passwd = request.REQUEST.get('user_passwd')
        if user_name is not None and user_passwd is not None:
            pwd = make_password(user_passwd, None, 'pbkdf2_sha256')
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            insert = {"user_name": user_name, 'user_passwd': pwd, 'client_ip': ip, 'auth_group': 1}
            u = usermodel()
            uid = u.insert(insert)
            if uid:
                return HttpResponseRedirect("/users/")
    return render(request, 'users/new_users.html', {})


@login_required
def getRoomById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    rm = roommodel()

    key_list = ['id', 'room_name', 'room_addr']

    r = rm.find({"id": id})

    result = Query.fSqlResult(r, key_list)

    ret = {'result': result[0]}

    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def deleteRoomById(request):
    id = request.REQUEST.get('id', None)
    result = {"ret": "delete faild"}
    if id:
        rm = roommodel()
        r = rm.delete({"id": id})
        result = {"ret": "delete success"}

    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
@csrf_protect
def new_room(request):
    name_tips = ""
    insert = {}
    if request.method == 'POST':
        room_name = request.REQUEST.get('room_name')
        room_addr = request.REQUEST.get('room_addr')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))

        insert = {"room_name": room_name, 'room_addr': room_addr}
        rm = roommodel()
        isF = isexist(rm, 'room_name', room_name)
        if isF == 1 and editor == 0:
            name_tips = "名称重复"

        elif room_name is not None and room_addr is not None:
            if editor and id:
                room_id = rm.update(insert, {"id": id})
            else:

                room_id = rm.insert(insert)
            if room_id:
                return HttpResponseRedirect("/room_list/?p=" + str(editor_current_page))
        else:
            name_tips = "参数错误"
    return render(request, 'room/new_room.html', {"val": insert, "name_tips": name_tips})


@login_required
@csrf_protect
def ajaxroomlist(request):
    page = request.REQUEST.get('p', 1)

    pageSize = request.REQUEST.get('pageSize', 6)

    key_list = ['id', 'room_name', 'room_addr']

    rm = roommodel()
    r = rm.find({})
    result = Query.fSqlResult(r, key_list)
    # rk = rackmodel()
    totalPage = rm.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    head = {'a_id': "自增序号", 'b_room_name': "机房名称", 'c_room_addr': "机房所在地址", "d_oper": "操作"}

    ret = {
        "body": result,
        "head": head,
        "page": {
            "current": page,
            "totalpage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


@login_required(login_url='/login/')
def room_list(request):
    key_list = ['id', 'room_name', 'room_addr']

    rm = roommodel()
    r = rm.find({})
    print
    r
    result = Query.fSqlResult(r, key_list)
    print
    result
    return render(request, 'room/room_list.html', {'ret': result})


@login_required
def getService_providerById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    svr = servicemodel()

    key_list = ['id', 'service_provider_name', 'service_provider_addr']

    # sql = Sql.get_s_sql('service_provider', key_list, {"id": id})

    r = svr.find({"id": id})

    result = Query.fSqlResult(r, key_list)

    ret = {'result': result[0]}

    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def deleteService_providerById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        svr = servicemodel()
        r = svr.delete({"id": id})
        result = {"ret": "delete success"}

    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
@csrf_protect
def new_service_provider(request):
    name_tips = ""
    insert = {}
    if request.method == 'POST':

        service_provider_name = request.REQUEST.get('service_provider_name')

        service_provider_addr = request.REQUEST.get('service_provider_addr')

        editor = int(request.REQUEST.get('editor', 0))

        id = int(request.REQUEST.get('id', 0))

        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))

        insert = {"service_provider_name": service_provider_name, 'service_provider_addr': service_provider_addr}

        svr = servicemodel()

        isF = isexist(svr, 'service_provider_name', service_provider_name)

        if isF == 1 and editor == 0:
            name_tips = "名称重复"
        elif service_provider_name is not None and service_provider_addr is not None:

            if editor and id:
                # sql = Sql.get_u_sql(table, insert, {"id": id})
                ret = svr.update(insert, {"id": id})
            else:
                # sql = Sql.get_i_sql(table, insert)
                ret = svr.insert(insert)

            if ret:
                return HttpResponseRedirect("/service_provider/?p" + str(editor_current_page))
        else:
            name_tips = "参数错误"
            # return HttpResponseRedirect("/service_provider/")
    return render(request, 'service/new_service_provider.html', {"val": insert, "name_tips": name_tips})


@login_required
def service_provider(request):
    key_list = ['id', 'service_provider_name', 'service_provider_addr']

    svr = servicemodel()

    r = svr.find({})

    result = Query.fSqlResult(r, key_list)

    return render(request, 'service/service_provider.html', {'ret': result})


@login_required
def ajax_service_provider(request):
    page = request.REQUEST.get('p', 1)

    pageSize = request.REQUEST.get('pageSize', 6)

    svr = servicemodel()

    key_list = ['id', 'service_provider_name', 'service_provider_addr']

    r = svr.find({})

    result = Query.fSqlResult(r, key_list)

    totalPage = svr.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    head = {'a_id': "自增序号", 'b_service_provider_name': "服务提供商名称", 'c_service_provider_addr': "服务提供商地址", "x_oper": "操作"}

    ret = {
        "body": result,
        "head": head,
        "page": {
            "current": page,
            "totalpage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


@login_required
def vm(request):
    key_list = ['id', 'hostname', 'manage_ip', 'other_ip', 'app_name', 'cpu', 'mem', 'disk', 'status',
                'hypervisor_host']
    # sql = Sql.get_s_sql('vm', key_list, {})
    v = vmmodel()
    r = v.find({})
    result = Query.fSqlResult(r, key_list)
    return render(request, 'vm/vm.html', {'ret': result})


@login_required
@csrf_protect
def new_vm(request):
    name_tips = ""
    insert = {}
    if request.method == 'POST':
        hostname = request.REQUEST.get('hostname')
        manage_ip = request.REQUEST.get('manage_ip')
        other_ip = request.REQUEST.get('other_ip')
        app_name = request.REQUEST.get('app_name')
        system_version = request.REQUEST.get('system_version')
        zabbix_template = request.REQUEST.get('zabbix_template')
        owner_group = request.REQUEST.get('owner_group')
        cpu = request.REQUEST.get('cpu')
        mem = request.REQUEST.get('mem')
        disk = request.REQUEST.get('disk')
        change_dev_info = request.REQUEST.get('change_dev_info')
        change_people = request.REQUEST.get('change_people')
        description = request.REQUEST.get('description')
        status = request.REQUEST.get('status')
        hypervisor_host = request.REQUEST.get('hypervisor_host')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))

        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))

        v = vmmodel()
        # table = 'vm'
        insert = {
            "hostname": hostname,
            'manage_ip': manage_ip,
            'other_ip': other_ip,
            'app_name': app_name,
            'system_version': system_version,
            'zabbix_template': zabbix_template,
            'owner_group': owner_group,
            'cpu': cpu,
            'mem': mem,
            'disk': disk,
            'description': description,
            'status': status,
            'hypervisor_host': hypervisor_host
        }

        if change_dev_info:
            insert['change_dev_info'] = change_dev_info
        if change_people:
            insert['change_people'] = change_people

        isF = isexist(v, 'hostname', hostname)
        if isF == 1 and editor == 0:
            name_tips = "名称重复"
        elif hostname and manage_ip:
            if editor and id:
                insert['change_time'] = time.time()

                efeck_row = v.update(insert, {"id": id})
            else:

                efeck_row = v.insert(insert)

            if efeck_row:
                return HttpResponseRedirect("/vm/?p=" + str(editor_current_page))
        else:
            name_tips = "参数错误"
    return render(request, 'vm/new_vm.html', {"server_group": ServerGroup.group, "val": insert, "name_tips": name_tips})


@login_required
def getVmById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    v = vmmodel()
    key_list = [
        'id',
        'hostname',
        'manage_ip',
        'other_ip',
        'app_name',
        'system_version',
        'zabbix_template',
        'owner_group',
        'cpu',
        'mem',
        'disk',
        'hypervisor_host',
        'change_time',
        'change_dev_info',
        'change_people',
        'description',
        'status'
    ]
    # sql = Sql.get_s_sql('vm', key_list, {"id": id})
    r = v.find({{"id": id}})
    result = Query.fSqlResult(r, key_list)
    ret = {'result': result[0], 'owner_group': ServerGroup.group}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required()
def deleteVmById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        v = vmmodel()
        r = v.delete({"id": id})
        if r:
            result = {"ret": "delete success"}

    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def ajax_vm(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)

    key_list = ['id',
                'hostname',
                'manage_ip',
                'other_ip',
                'app_name',
                'system_version',
                'zabbix_template',
                'owner_group',
                'cpu',
                'mem',
                'disk',
                'hypervisor_host',
                'change_time',
                'change_dev_info',
                'change_people',
                'description',
                'status'
                ]

    v = vmmodel()
    r = v.find({})
    result = Query.fSqlResult(r, key_list)

    totalPage = v.count({})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    head = {
        'a_id': "自增序号",
        'b_hostname': "虚拟主机名称",
        'c_manage_ip': "管理IP",

        'i_cpu': "CPU",
        'j_mem': '内存',
        'k_disk': "硬盘",
        'l_hypervisor_host': "宿主机地址",
        'r_oper': "操作"
    }
    ret = {
        "body": result,
        "head": head,
        "page": {
            "current": page,
            "totalpage": totalPage,
            "lastpage": totalPage
        }
    }
    return HttpResponse(json.dumps(ret, sort_keys=True), content_type="application/json")


def logout_view(requst):
    logout(requst)
    return HttpResponseRedirect("/login/")


# @login_required
@csrf_protect
def login(request):
    login_form = LoginForm()
    return render(request, 'registration/login.html', {'form': login_form})


def check_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('registration/login.html', RequestContext(request, {'form': form, }))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('user_name', '')
            password = request.POST.get('passs_word', '')

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/index/")
                # return render_to_response('index.html', RequestContext(request))
            else:
                return render_to_response('registration/login.html',
                                          RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:
            return render_to_response('registration/login.html', RequestContext(request, {'form': form, }))


def page_not_found(request):
    return render_to_response('404.html')


def page_error(request):
    return render_to_response('500.html')
