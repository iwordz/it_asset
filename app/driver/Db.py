__author_ = 'fanghouguo'

'''
  mysql basic driver
  manager mysql base systax in select,delete isnert into
'''

from  django.db import connection
import MySQLdb

class Db(object):

    conn  =  None
    cur  =  None
    instance  =  None

    '''
      init mysql connect
    '''
    def __init__(self):
        self.conn = connection
        self.cur = self.conn.cursor()

    ''' 
      delete table data
    '''

    def delete(self,table,data):
        del_data_sql = "delete from %s " % table
        del_data_sql += self.dict_2_str_and(data)
        return self.cur.execute(del_data_sql)

    ''' 
      return json object
    '''

    def find(self,table,data):
        sql = "select * from %s " % table
        sql += self.dict_2_str_and(data)
        self.cur.execute(sql)
        rawData = self.cur.fetchall()
        col_names = [desc[0] for desc in self.cur.description]
        result = []
        for row in rawData:
            objDict = {}
            for index, value in enumerate(row):
                objDict[col_names[index]] = value
            result.append(objDict)

        return result

    '''
     
    '''
    def fSqlResult(self,r, key_list):
        mlist = []
        l = len(key_list)
        if r:
            for item in r:
                tmp = {}
                for i in range(l):
                    tmp[key_list[i]] = str(item[i])
                mlist.append(tmp)
        return mlist


    '''
      insert into table data
    '''
    def insert(self,table,data):
        insert_data_sql = self.dict_2_str_and(data)
        return  self.cur.execute(insert_data_sql)


    '''
       dic transfer string
    '''
    def dict_2_str(self,dictin):

        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (str(k), self.safe(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ','.join(tmplist)

    def dict_2_str_and(self,dictin):

        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (str(k), self.safe(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ' and '.join(tmplist)

    def safe(self,s):
        return MySQLdb.escape_string(s)

    def get_count(self,table, condition):
        sql = 'select * from %s ' % table
        if condition:
            sql += ' where %s ' % self.dict_2_str_and(condition)
        print "count sql=" + str(sql)
        r = self.cur.execute(sql)
        return r
        #return len(r)

    def get_i_sql(self,table, dict):
        sql = 'insert into %s set ' % table
        sql += self.dict_2_str(dict)
        return sql

    def get_s_sql(self,table, keys, conditions, page=0, pagesize=3, isdistinct=0):

        if isdistinct:
            sql = 'select distinct %s ' % ",".join(keys)
        else:
            sql = 'select  %s ' % ",".join(keys)
        sql += ' from %s ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        if page:
            offset = (int(page) - 1) * pagesize
            sql += 'limit %s' % offset
            sql += ',%s' % pagesize
        return sql

    def get_u_sql(self,table, value, conditions):

        sql = 'update %s set ' % table
        sql += self.dict_2_str(value)
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql

    def get_d_sql(self,table, conditions):

        sql = 'delete from  %s  ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql

    def close(self):
        self.conn.close()
        self.cur.close()
