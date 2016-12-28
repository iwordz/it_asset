#coding=utf-8
__author__ = 'fanghouguo'
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
import Query,Sql,ServerGroup,time,UserTime,MakeHtml,json
from app.forms import *
from SqlConn import SqlConn

# dashbord page
@login_required
def index(request):
    conn = SqlConn()
    room_num = Sql.get_count(conn, 'Room', {})
    rack_num = Sql.get_count(conn, 'Idc', {})
    server_num = Sql.get_count(conn, 'Server', {})
    vm_num = Sql.get_count(conn, 'VM', {})
    online_num = Sql.get_count(conn, 'Server', {"status":1})
    offline_num = server_num - Sql.get_count(conn, 'Server', {"status":1})
    return render(request, 'index.html', {"room":room_num,'rack':rack_num,'server':server_num,'vm':vm_num,'online':online_num,'offline':offline_num})

@login_required
def deleteRackById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('Idc', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def getRackById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']
    sql = Sql.get_s_sql('Idc', key_list, {"id": id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'Service_provider_name']
    sql_1 = Sql.get_s_sql('Service_provider', key_list_1, {})
    r_1 = conn.execute(sql_1)
    servers = Query.fSqlResult(r_1, key_list_1)

    ret = {'result': result[0], 'sel': servers}

    return HttpResponse(json.dumps(ret), content_type="application/json")
    # html = MakeHtml.makeFormTable(result)
    # return render(request, 'test.html', {'ret': html})

@login_required
#test make html
def html(request):
    id = request.REQUEST.get('id', None)
    if id is None:
        return render(request, 'test.html', {})
    conn = SqlConn()
    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']
    sql = Sql.get_s_sql('Idc', key_list, {"id": id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    html = MakeHtml.makeFormTable(result)
    return render(request, 'test.html', {'ret': html})




@login_required
@csrf_protect
def ajax_rack_list(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']
    sql = Sql.get_s_sql('Idc', key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'Idc', {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    key_list_1 = ['id', 'Service_provider_name']
    sql_1 = Sql.get_s_sql('Service_provider', key_list_1, {})
    r_1 = conn.execute(sql_1)
    servers = Query.fSqlResult(r_1, key_list_1)
    # print servers
    new_service = {}
    for srv in servers:
        for id in srv:
            print id
            if id == 'id':
                new_service[srv[id]] = srv['Service_provider_name']

    new_result = []
    for item in result:
        item['service_provider'] = new_service[item['service_provider']]
        item['start_time'] = UserTime.utcToString(float(item['start_time']))
        item['end_time'] = UserTime.utcToString(float(item['end_time']))
        new_result.append(item)
    print new_result
    conn.close()

    # contexts = {'ret': result,'totalpage':totalPage,'current':page,'lastPage':totalPage}
    # print "current page="+ str(page)
    # return render_to_response('rack_list.html', contexts)
    #return render(request, 'rack_list.html',
    #              {'ret': result, 'totalpage': totalPage, 'current': page, 'lastPage': totalPage})

    #head = {'a_id':"id", 'b_idc_name':"idc_name", 'c_rack_number':"rack_number", 'd_start_time':"start_time", 'e_end_time':"end_time", 'f_service_provider':"service_provider","x_oper":"oper"}
    head = {'a_id':"自增序号", 'b_idc_name':"机柜名称", 'c_rack_number':"机柜编号", 'd_start_time':"开始时间", 'e_end_time':"结束时间", 'f_service_provider':"服务提供商","x_oper":"操作"}

    ret = {
        "body": result,
        "head": head,
        "page" : {
            "current" : page,
            "totalpage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")




@login_required
@csrf_protect
def rack_jgt(request):
    conn = SqlConn()
    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']
    sql = Sql.get_s_sql('Idc', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    #print "result:"+str(result)
    key_list_1 = ['id', 'hostname', 'manage_ip', 'other_ip', 'app_name', 'cpu', 'mem', 'disk', 'sn', 'an', 'units',
                'idc_name', 'rack_number', 'rack_units', 'status','system_version']
    new_result = []
    for srv in result:
      sql_1 = Sql.get_s_sql('Server', key_list_1, {"idc_name":srv['id']})
      r_1 = conn.execute(sql_1)
      servers = Query.fSqlResult(r_1, key_list_1)
      idc_name = srv['idc_name']
      new_result.append([idc_name,servers])

    conn.close()
    return render(request, 'rack/rack_demo.html',
                  {'ret': new_result})


@login_required
@csrf_protect
def rack_list(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = ['id', 'idc_name', 'rack_number', 'start_time', 'end_time', 'service_provider']
    sql = Sql.get_s_sql('Idc', key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'Idc', {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize

    key_list_1 = ['id', 'Service_provider_name']
    sql_1 = Sql.get_s_sql('Service_provider', key_list_1, {})
    r_1 = conn.execute(sql_1)
    servers = Query.fSqlResult(r_1, key_list_1)
    # print servers
    new_service = {}
    for srv in servers:
        for id in srv:
            print id
            if id == 'id':
                new_service[srv[id]] = srv['Service_provider_name']

    new_result = []
    for item in result:
        item['service_provider'] = new_service[item['service_provider']]
        item['start_time'] = UserTime.utcToString(float(item['start_time']))
        item['end_time'] = UserTime.utcToString(float(item['end_time']))
        new_result.append(item)
    #print new_result
    conn.close()


    return render(request, 'rack/rack_list.html',
                  {'ret': result, 'totalpage': totalPage, 'current': page, 'lastPage': totalPage})

@login_required
@csrf_protect
def del_rack(request):
    pass

@login_required
@csrf_protect
def new_rack(request):
    if request.method == 'POST':
        idc_name = request.REQUEST.get('idc_name')
        rack_number = request.REQUEST.get('rack_number')
        start_time = request.REQUEST.get('start_time')
        end_time = request.REQUEST.get('end_time')
        service_provider = request.REQUEST.get('service_provider')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))
        print idc_name, rack_number, start_time, end_time, service_provider
        print  "editor=" + str(editor), "id=" + str(id)
        if idc_name is not None and rack_number is not None:
            start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_time = time.mktime(start_time)
            end_time = time.mktime(end_time)
            if start_time > end_time:
                return
            table = 'Idc'
            insert = {"idc_name": idc_name, 'rack_number': rack_number, 'start_time': start_time, 'end_time': end_time,
                      'service_provider': service_provider}
            if editor and id:
                sql = Sql.get_u_sql(table, insert, {"id": id})
            else:
                sql = Sql.get_i_sql(table, insert)
            print sql
            conn = SqlConn()
            conn.execute(sql)
            if editor and id:
                rack_id = 1
            else:
                rack_id = conn.last_id(table)
            conn.commit()
            conn.close()
            if rack_id:
                return HttpResponseRedirect("/rack_list/?p=" + str(editor_current_page))
    else:
        pass
    conn = SqlConn()
    key_list = ['id', 'Service_provider_name']
    sql = Sql.get_s_sql('Service_provider', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    conn.close()
    # print result
    return render(request, 'rack/new_rack.html', {'service_provider_list': result})

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
        print idc_name, rack_number, start_time, end_time, service_provider
        if idc_name is not None and rack_number is not None:
            start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_time = time.mktime(start_time)
            end_time = time.mktime(end_time)
            if start_time > end_time:
                return

            insert = {"idc_name": idc_name, 'rack_number': rack_number, 'start_time': start_time, 'end_time': end_time,
                      'service_provider': service_provider}
            table = 'Idc'
            sql = Sql.get_i_sql(table, insert)
            conn = SqlConn()
            conn.execute(sql)
            rack_id = conn.last_id(table)
            conn.commit()
            conn.close()
            if rack_id:
                return HttpResponseRedirect("/rack_list/")
    else:
        pass
    conn = SqlConn()
    key_list = ['id', 'room_name']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    sql_1 = Sql.get_s_sql('Idc', key_list_1, {})
    r_1 = conn.execute(sql_1)
    result_1 = Query.fSqlResult(r_1, key_list_1)

    conn.close()
    print result
    return render(request, 'new__config.html', {'room_list': result, 'rack_list': result_1})




########################################## start networking

@login_required
def network_config(request):
    conn = SqlConn()
    key_list = ['id', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units', 'rack_number',
                'rack_units']
    sql = Sql.get_s_sql('network_config', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    conn.close()
    return render(request, 'network/network_config.html', {'ret': result})

@login_required
@csrf_protect
def new_network_config(request):
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
        print "editor="+str(editor)+",id="+str(id)+',editor_current_page='+str(editor_current_page)
        if idc_name is not None and rack_number is not None:

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
            if editor and id:
              sql = Sql.get_u_sql(table,insert,{"id":id})
            else:
              sql = Sql.get_i_sql(table, insert)
            conn = SqlConn()
            conn.execute(sql)
            if editor and id:
              rack_id = 1
            else:
             rack_id = conn.last_id(table)
            conn.commit()
            conn.close()
            if rack_id:
                return HttpResponseRedirect("/network_config/?p"+str(editor_current_page))
    else:
        pass
    conn = SqlConn()
    key_list = ['id', 'room_name']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    sql_1 = Sql.get_s_sql('Idc', key_list_1, {})
    r_1 = conn.execute(sql_1)
    result_1 = Query.fSqlResult(r_1, key_list_1)

    conn.close()
    print result
    # return render(request, 'new__config.html', {'room_list':result,'rack_list':result_1})
    return render(request, 'network/new_network_config.html', {'room_list': result, 'rack_list': result_1})


@login_required
def getNetwork_configById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
    key_list = ['id','device_name', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units', 'rack_number',
                'rack_units']
    sql = Sql.get_s_sql('network_config', key_list, {"id":id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    conn.close()

    conn = SqlConn()
    key_list = ['id', 'room_name']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    room = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    sql_1 = Sql.get_s_sql('Idc', key_list_1, {})
    r_1 = conn.execute(sql_1)
    idc = Query.fSqlResult(r_1, key_list_1)

    ret = {'result': result[0],'idc' : idc,'room' : room}
    return HttpResponse(json.dumps(ret), content_type="application/json")

@login_required
def deleteNetwork_configById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('network_config', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")
@login_required
def ajax_network_config(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = ['id','device_name', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units', 'rack_number',
                'rack_units']
    sql = Sql.get_s_sql('network_config', key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'network_config', {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize
    conn.close()


    conn = SqlConn()
    key_list = ['id', 'room_name']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    room = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    sql_1 = Sql.get_s_sql('Idc', key_list_1, {})
    r_1 = conn.execute(sql_1)
    idc = Query.fSqlResult(r_1, key_list_1)

    conn.close()

    # head = {
    #     'a_id':"id",
    #     'b_idc_name':"idc_name",
    #     'c_manage_ip':"manage_ip",
    #     'd_other_ip':"other_ip",
    #     #'e_dev_type':"dev_type",
    #     #'f_dev_ports':"dev_ports",
    #     #'g_sn':"sn",
    #     #'h_an':"an",
    #     #'i_units':"units",
    #     'j_rack_number':"rack_number",
    #     'k_rack_units':"rack_units",
    #     "x_oper":"oper"
    # }

    head = {
        'a_id':"自增序号",
        'b_device_name':"设备名称",
        'c_idc_name':"所在机房",
        'd_manage_ip':"管理IP",
        'e_other_ip':"非管理IP",
        #'e_dev_type':"dev_type",
        #'f_dev_ports':"dev_ports",
        #'g_sn':"sn",
        #'h_an':"an",
        #'i_units':"units",
        'j_rack_number':"所在机柜",
        'k_rack_units':"机柜编号",
        "x_oper":"操作"
    }
    new_room = {}
    for j in room:
        new_room[j['id']] = j['room_name']
    new_idc = {}
    for k in idc:
        new_idc[k['id']] = k['idc_name']
    new_result = []
    for item in result:
        item['idc_name'] = new_room[item['idc_name']]
        item['rack_number'] = new_idc[item['rack_number']]
        new_result.append(item)
    ret = {
        "body": new_result,
        "head": head,
        "idc" : idc,
        'room' : room,
        "page" : {
            "current" : page,
            "totalpage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")

########################################## end networking


########################################## server start

@login_required
def getServerById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
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
    sql = Sql.get_s_sql('Server', key_list, {"id": id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    conn = SqlConn()
    key_list = ['id', 'room_name']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    room = Query.fSqlResult(r, key_list)

    key_list_1 = ['id', 'idc_name']
    sql_1 = Sql.get_s_sql('Idc', key_list_1, {})
    r_1 = conn.execute(sql_1)
    idc = Query.fSqlResult(r_1, key_list_1)
    #print "idc="+str(idc)
    #print "result="+str(result)
    ret = {'result': result[0],'idc' : idc,'room' : room,'owner_group' : ServerGroup.group,'server_type' : ServerGroup.type}
    print "ret="+str(ret)
    return HttpResponse(json.dumps(ret), content_type="application/json")

@login_required
def deleteServerById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('Server', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")


#@login_required()
def server(request):
    conn = SqlConn()
    key_list = ['id', 'hostname', 'manage_ip', 'other_ip', 'app_name', 'cpu', 'mem', 'disk', 'sn', 'an', 'units',
                'idc_name', 'rack_number', 'rack_units', 'status']
    sql = Sql.get_s_sql('Server', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    # head = ['id', 'host name', 'manager ip', 'other IP', 'app nane', 'CPU', 'memory', 'disk', 'sn', 'an', 'units',
    #         'room', 'rack', 'rack number', 'status', 'oper']
    head = ['id', 'host name', 'manager ip', 'other IP', 'app nane', 'CPU', 'memory', 'disk', 'sn', 'an', 'units',
            'room', 'rack', 'rack number', 'status', 'oper']
    return render(request, 'server/server.html', {'ret': result, 'data': result, 'head': head, 'body': result})
    # ret = {"body":result,"head":head}
    # return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def ajaxserver(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = [
        'id',
        'hostname',
        'manage_ip',
        'other_ip',
        'app_name',
        'cpu', 'mem', 'disk', 'sn', 'an', 'units',
                'idc_name', 'rack_number', 'rack_units', 'status']
    sql = Sql.get_s_sql('Server', key_list, {},page,pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'Idc', {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize
    # head = {
    #     'a_id': "id",
    #     'b_hostname': "hostname",
    #     'c_manage_ip': "manage_ip",
    #     'd_other_ip': "other_ip",
    #     #'e_app_name': "app_name",
    #     'f_cpu': "cpu",
    #     'g_mem': "mem",
    #     'h_disk': "disk",
    #     #'i_sn': "sn",
    #     #'j_an': "an",
    #     #'k_units': "units",
    #     #'l_idc_name': "idc_name",
    #     #'m_rack_number': "rack_number",
    #     #'n_rack_units': "rack_units",
    #     'o_status': "status",
    #     'p_oper': "oper"
    # }
    head = {
        'a_id': " 自增序号",
        'b_hostname': "主机名称",
        'c_manage_ip': "管理IP",
        'd_other_ip': "非管理IP",
        #'e_app_name': "app_name",
        'f_cpu': "CPU",
        'g_mem': "内存",
        'h_disk': "硬盘",
        #'i_sn': "sn",
        #'j_an': "an",
        #'k_units': "units",
        #'l_idc_name': "idc_name",
        #'m_rack_number': "rack_number",
        #'n_rack_units': "rack_units",
        'o_status': "状态",
        'p_oper': "操作"
    }
    # return render(request, 'server.html', {'ret':result,'data':result,'head':head,'body':result})
    ret = {
        "body": result,
        "head": head,
        "page" : {
            "current" : page,
            "totalPage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")


@login_required
@csrf_protect
def new_server(request):
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
        #change_time = request.REQUEST.get('change_time',None)
        change_dev_info = request.REQUEST.get('change_dev_info',None)
        change_people = request.REQUEST.get('change_people',None)
        description = request.REQUEST.get('description')
        status = request.REQUEST.get('status')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))
        print "editor="+str(editor)+",id="+str(id)+',editor_current_page='+str(editor_current_page)
        conn = SqlConn()

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
        if editor and id:
            insert['change_time'] = time.time()
        if change_dev_info:
            insert['change_dev_info'] = change_dev_info
        if change_people:
            insert['change_people'] = change_people
        table = 'Server'
        if editor and id:
         afeck_row =  1
         sql = Sql.get_u_sql(table,insert,{"id":id})
        else:
         sql = Sql.get_i_sql(table, insert)
        r = conn.execute(sql)
        if editor and id:
            afeck_row =  1
        else:
            afeck_row = conn.last_id(table)
        if afeck_row:
            return HttpResponseRedirect("/server/?p="+str(editor_current_page))
    conn = SqlConn()
    key_list = ['id', 'room_name']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    key_list_1 = ['id', 'idc_name']
    sql_1 = Sql.get_s_sql('Idc', key_list_1, {})
    r_1 = conn.execute(sql_1)
    result_1 = Query.fSqlResult(r_1, key_list_1)

    server_group = ServerGroup.group
    server_type = ServerGroup.type
    key_list_2 = ['id', 'idc_name', 'manage_ip', 'other_ip', 'dev_type', 'dev_ports', 'sn', 'an', 'units', 'rack_number',
                'rack_units']
    sql_2 = Sql.get_s_sql('network_config', key_list_2, {})
    r_2 = conn.execute(sql_2)
    result_2 = Query.fSqlResult(r_2, key_list_2)
    conn.close()
    return render(request, 'server/new_server.html', {'server_group':server_group,'server_type':server_type,'room_list': result, 'rack_list': result_1,'network':result_2})

########################################## server end

@login_required
def statistics(request):
    return render(request, 'statistics.html', {})



@login_required
def users(request):
    conn = SqlConn()
    key_list = ['id', 'username', 'is_active', 'date_joined','email','last_login']
    sql = Sql.get_s_sql('auth_user', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    conn.close()
    # return render(request, 'rack_list.html', {'ret': result})
    return render(request, 'users/users.html', {'ret': result})

@login_required
@csrf_protect
def ajax_users(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = ['id', 'username', 'is_active', 'date_joined','email','last_login']
    sql = Sql.get_s_sql('auth_user', key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'auth_user', {})

    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize
    conn.close()
    #head = {'a_id':"id", 'b_room_name':"room_name", 'c_room_addr':"room_addr","d_oper":"oper"}
    head = {'a_id':"用户ID", 'b_username':"用户名称", 'c_is_active':"是否可用", 'd_date_joined':"加入时间", 'e_email':"邮件",'f_last_login':"最后登录"}
    new_result = []
    for i in result:
        if i['is_active']:
            i['is_active'] = '可用'
        new_result.append(i);
    ret = {
        "body": new_result,
        "head": head,
        "page" : {
            "current" : page,
            "totalpage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")


@login_required
def deleteUsersById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('auth_user', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def getUsersById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
    key_list = ['id', 'username', 'is_active', 'date_joined','email','last_login']
    sql = Sql.get_s_sql('auth_user', key_list, {"id": id})
    r = conn.execute(sql)
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
            table = 'users'
            sql = Sql.get_i_sql(table, insert)
            conn = SqlConn()
            conn.execute(sql)
            uid = conn.last_id(table)
            conn.commit()
            conn.close()
            if uid:
                return HttpResponseRedirect("/users/")
    return render(request, 'users/new_users.html', {})



@login_required
def getRoomById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
    key_list = ['id', 'room_name', 'room_addr']
    sql = Sql.get_s_sql('Room', key_list, {"id": id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    ret = {'result': result[0]}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def deleteRoomById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('Room', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
@csrf_protect
def new_room(request):
    if request.method == 'POST':
        room_name = request.REQUEST.get('room_name')
        room_addr = request.REQUEST.get('room_addr')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))
        print "editor="+str(editor)+",id="+str(id)+',editor_current_page='+str(editor_current_page)
        if room_name is not None and room_addr is not None:
            insert = {"room_name": room_name, 'room_addr': room_addr}
            table = 'Room'
            if editor and id:
               sql = Sql.get_u_sql(table,insert,{'id':id})
            else:
               sql = Sql.get_i_sql(table,insert)
            conn = SqlConn()
            conn.execute(sql)
            conn.commit()
            if editor and id:
                room_id = 1
            else:
                room_id = conn.last_id(table)
            if room_id:
                conn.close()
                return HttpResponseRedirect("/room_list/?p="+str(editor_current_page))
    return render(request, 'room/new_room.html', {})



@login_required
@csrf_protect
def ajaxroomlist(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = ['id', 'room_name', 'room_addr']
    sql = Sql.get_s_sql('Room', key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'Idc', {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize
    conn.close()
    #head = {'a_id':"id", 'b_room_name':"room_name", 'c_room_addr':"room_addr","d_oper":"oper"}
    head = {'a_id':"自增序号", 'b_room_name':"机房名称", 'c_room_addr':"机房所在地址","d_oper":"操作"}

    ret = {
        "body": result,
        "head": head,
        "page" : {
            "current" : page,
            "totalpage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")



@login_required(login_url='/login/')
def room_list(request):
    # return render(request, 'room_list.html', {})
    conn = SqlConn()
    key_list = ['id', 'room_name', 'room_addr']
    sql = Sql.get_s_sql('Room', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    conn.close()
    # return render(request, 'rack_list.html', {'ret': result})
    return render(request, 'room/room_list.html', {'ret': result})



############################################ start Service_providerById
@login_required
def getService_providerById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
    key_list = ['id', 'service_provider_name', 'service_provider_addr']
    sql = Sql.get_s_sql('Service_provider', key_list, {"id": id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    ret = {'result': result[0]}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required
def deleteService_providerById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('Service_provider', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
@csrf_protect
def new_service_provider(request):
    if request.method == 'POST':
        service_provider_name = request.REQUEST.get('service_provider_name')
        service_provider_addr = request.REQUEST.get('service_provider_addr')
        editor = int(request.REQUEST.get('editor', 0))
        id = int(request.REQUEST.get('id', 0))
        editor_current_page = int(request.REQUEST.get('editor_current_page', 1))
        print "editor="+str(editor)+",id="+str(id)+',editor_current_page='+str(editor_current_page)
        if service_provider_name is not None and service_provider_addr is not None:
            insert = {"service_provider_name": service_provider_name, 'service_provider_addr': service_provider_addr}
            table = 'Service_provider'
            if editor and id:
                sql = Sql.get_u_sql(table,insert,{"id":id})
            else:
                sql = Sql.get_i_sql(table, insert)

            conn = SqlConn()
            conn.execute(sql)

            if editor and id:
             uid = 1
            else:
             uid = conn.last_id(table)
            conn.commit()
            conn.close()
            if uid:
                return HttpResponseRedirect("/service_provider/?p"+str(editor_current_page))
                #return HttpResponseRedirect("/service_provider/")
    return render(request, 'service/new_service_provider.html', {})



@login_required
def service_provider(request):
    conn = SqlConn()
    key_list = ['id', 'service_provider_name', 'service_provider_addr']
    sql = Sql.get_s_sql('service_provider', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    conn.close()
    # return render(request, 'rack_list.html', {'ret': result})
    return render(request, 'service/service_provider.html', {'ret': result})



@login_required
def ajax_service_provider(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
    key_list = ['id', 'service_provider_name', 'service_provider_addr']
    sql = Sql.get_s_sql('Service_provider', key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, 'Service_provider', {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize
    conn.close()
    #head = {'a_id':"id", 'b_service_provider_name':"service_provider_name", 'c_service_provider_addr':"service_provider_addr","x_oper":"oper"}
    head = {'a_id':"自增序号", 'b_service_provider_name':"服务提供商名称", 'c_service_provider_addr':"服务提供商地址","x_oper":"操作"}

    ret = {
        "body": result,
        "head": head,
        "page" : {
            "current" : page,
            "totalpage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")
############################################ end Service_providerById

############################################ start vm


@login_required
def vm(request):
    conn = SqlConn()
    key_list = ['id', 'hostname', 'manage_ip', 'other_ip', 'app_name', 'cpu', 'mem', 'disk', 'status',
                'hypervisor_host']
    sql = Sql.get_s_sql('VM', key_list, {})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    return render(request, 'vm/vm.html', {'ret': result})


@login_required
@csrf_protect
def new_vm(request):
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
        print "editor="+str(editor)+",id="+str(id)+',editor_current_page='+str(editor_current_page)
        conn = SqlConn()

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
        if   change_people:
             insert['change_people'] = change_people

        table = 'VM'
        if editor and id:
           sql = Sql.get_u_sql(table,insert,{"id":id})
        else:
           sql = Sql.get_i_sql(table, insert)
        conn.execute(sql)

        if editor and id:
            efeck_row = 1
        else:
            efeck_row = conn.last_id(table)
        if efeck_row:
            return HttpResponseRedirect("/vm/?p="+str(editor_current_page))
    return render(request, 'vm/new_vm.html', {"server_group":ServerGroup.group})



@login_required
def getVmById(request):
    id = request.REQUEST.get('id', None)
    result = {}
    if id is None or id == 0:
        return HttpResponse(json.dumps(result), content_type="application/json")
    conn = SqlConn()
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
    sql = Sql.get_s_sql('VM', key_list, {"id": id})
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)
    ret = {'result': result[0],'owner_group':ServerGroup.group}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required()
def deleteVmById(request):
    id = request.REQUEST.get('id', None)
    page = request.REQUEST.get('p', 1)
    result = {"ret": "delete faild"}
    if id:
        conn = SqlConn()
        sql = Sql.get_d_sql('VM', {"id": id})
        r = conn.execute(sql)
        result = {"ret": "delete success"}
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def ajax_vm(request):
    page = request.REQUEST.get('p', 1)
    pageSize = request.REQUEST.get('pageSize', 6)
    conn = SqlConn()
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
    table = "VM"
    sql = Sql.get_s_sql(table, key_list, {}, page, pageSize)
    r = conn.execute(sql)
    result = Query.fSqlResult(r, key_list)

    totalPage = Sql.get_count(conn, table, {})
    print "totalPage2=" + str(totalPage)
    if totalPage % pageSize:
        totalPage = totalPage / pageSize + 1
    else:
        totalPage = totalPage / pageSize
    conn.close()
    # head = {
    #             'a_id':"id",
    #             'b_hostname':"hostname",
    #             'c_manage_ip':"manage_ip",
    #             #'d_other_ip':"other_ip",
    #             #'e_app_name':"app_name",
    #             #'f_system_version' : "system_version",
    #             #'g_zabbix_template' : "zabbix_template",
    #             #'h_owner_group' : "owner_group",
    #             'i_cpu' :"cpu",
    #             'j_mem'  : 'mem',
    #             'k_disk' : "disk",
    #             'l_hypervisor_host' : "hypervisor_host",
    #             #'m_change_time' : "change_time",
    #             #'n_change_dev_info' : "change_dev_info",
    #             #'o_change_people' : "change_people",
    #             #'p_description' : "description",
    #             #'q_status' : "status"
    #             'r_oper':"oper"
    # }
    head = {
                'a_id':"自增序号",
                'b_hostname':"虚拟主机名称",
                'c_manage_ip':"管理IP",
                #'d_other_ip':"other_ip",
                #'e_app_name':"app_name",
                #'f_system_version' : "system_version",
                #'g_zabbix_template' : "zabbix_template",
                #'h_owner_group' : "owner_group",
                'i_cpu' :"CPU",
                'j_mem'  : '内存',
                'k_disk' : "硬盘",
                'l_hypervisor_host' : "宿主机地址",
                #'m_change_time' : "change_time",
                #'n_change_dev_info' : "change_dev_info",
                #'o_change_people' : "change_people",
                #'p_description' : "description",
                #'q_status' : "status"
                'r_oper':"操作"
    }
    ret = {
        "body": result,
        "head": head,
        "page" : {
            "current" : page,
            "totalpage" : totalPage,
            "lastpage" : totalPage
        }
    }
    return HttpResponse(json.dumps(ret,sort_keys=True), content_type="application/json")

def logout_view(requst):
    logout(requst)
    return HttpResponseRedirect("/login/")

#@login_required
@csrf_protect
def login(request):
    login_form = LoginForm()
    return render(request, 'registration/login.html', {'form': login_form})

def check_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('registration/login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('user_name', '')
            password = request.POST.get('passs_word', '')
            print username,password
            user = auth.authenticate(username=username, password=password)
            print "user="+str(user)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/index/")
                #return render_to_response('index.html', RequestContext(request))
            else:
                return render_to_response('registration/login.html', RequestContext(request, {'form': form,'password_is_wrong':True}))
        else:
            return render_to_response('registration/login.html', RequestContext(request, {'form': form,}))
#@login_required
# def check_login(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user_name = login_form.cleaned_data['user_name']
#             pass_word = login_form.cleaned_data['passs_word']
#             if user_name and pass_word:
#                 conn = SqlConn()
#                 key_list = ['user_name', 'user_passwd']
#                 condtion = {"user_name": user_name}
#                 sql = Sql.get_s_sql('Users', key_list, condtion)
#                 r = conn.execute(sql)
#                 result = Query.fSqlResult(r, key_list)
#                 conn.close()
#                 pwd = make_password(pass_word, None, 'pbkdf2_sha256')
#                 d_pwd = result[0]['user_passwd']
#                 print pwd
#                 d_pwd = make_password(d_pwd, None, 'pbkdf2_sha256')
#                 p_bool = check_password(pwd, d_pwd)
#                 p_bool = True
#                 if p_bool:
#                     return HttpResponseRedirect("/index/")
#     else:
#         login_form = LoginForm()
#     return render(request, 'login.html', {'form': login_form})