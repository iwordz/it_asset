#encoding = 'utf-8'
__author__ = 'fanghouguo'

from basemodel import basemodel

class roommodel(basemodel):

    db = None

    table = "room"


    def __init__(self):
         super(roommodel, self).__init__()

    def count(self,where):
        return self.db.get_count(self.table,where)

    def insert(self,data):
        return self.db.insert(self.table,data)
    def update(self,value,where):
        return self.db.get_u_sql(self.table,value,where)
    def delete(self,where):
        return self.db.delete(self.table,where)

    def find(self,where):
        return self.db.find(self.table,where)
