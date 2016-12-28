#coding=utf-8
__author__ = 'fanghouguo'

#from django.http import HttpResponse
#from anyjson import serialize
#from django.http import HttpResponse

import MySQLdb

def safe(s):
    return MySQLdb.escape_string(s)



def get_count(conn,table,condition):
    sql = 'select * from %s ' % table
    if condition:
        sql += ' where %s ' % dict_2_str_and(condition)
    print "count sql="+str(sql)
    r = conn.execute(sql)
    return len(r)

def get_i_sql(table, dict):
    sql = 'insert into %s set ' % table
    sql += dict_2_str(dict)
    return sql


def get_s_sql(table, keys, conditions, page = 0,pagesize = 3,isdistinct=0):


    if isdistinct:
        sql = 'select distinct %s ' % ",".join(keys)
    else:
        sql = 'select  %s ' % ",".join(keys)
    sql += ' from %s ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    if page:
        offset = (int(page) - 1) * pagesize
        sql += 'limit %s' % offset
        sql += ',%s' % pagesize
    return sql


def get_u_sql(table, value, conditions):

    sql = 'update %s set ' % table
    sql += dict_2_str(value)
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql


def get_d_sql(table, conditions):

    sql = 'delete from  %s  ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql


def dict_2_str(dictin):

    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), safe(str(v)))
        tmplist.append(' ' + tmp + ' ')
    return ','.join(tmplist)


def dict_2_str_and(dictin):

    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), safe(str(v)))
        tmplist.append(' ' + tmp + ' ')
    return ' and '.join(tmplist)