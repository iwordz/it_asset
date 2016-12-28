#coding=utf-8
__author__ = 'fanghouguo'

from  django.db import connection

class SqlConn():
    def __init__(self):
        self.conn = connection
        self.cur = self.conn.cursor()
    def cur(self):
        return self.cur()
    def commit(self):
        self.conn.commit()
    def execute(self,sql,fetchone=0):
        self.cur.execute(sql)
        return self.cur.fetchone() if fetchone else self.cur.fetchall()
    def last_id(self,table):
        sql='SELECT LAST_INSERT_ID() from %s'%table
        return self.execute(sql,1)[0]
    def close(self):
        self.cur.close()
        self.conn.close()