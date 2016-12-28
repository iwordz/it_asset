#coding=utf-8
__author__ = 'fanghouguo'
from django.db import  connection,transaction

''' execute django sql '''

def query(sql):
    pass


''' return json object'''
def find(sql):
    #db = MySQLdb.connect(user='root', db='it_asset', passwd='12345678', host='localhost', charset='utf8')
    cursor = connection.cursor()
    cursor.execute(sql)
    rawData = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    result = []
    for row in rawData:
       objDict = {}
       for index ,value in enumerate(row):
           objDict[col_names[index]] = value
       result.append(objDict)
    return result



def fSqlResult(r,key_list):
    mlist=[]
    l=len(key_list)
    if r:
        for item in r:
            tmp={}
            for i in range(l):
                tmp[key_list[i]]=str(item[i])
            mlist.append(tmp)
    return mlist
