encoding = 'utf-8'

__author__ = 'fanghouguo'

import sys

class basemodel(object):

    db = None

    def __init__(self):
        load_path = sys.path[0] + "/app/driver/"
        #print load_path
        sys.path.append(load_path)
        #print sys.path
        from Db import Db
        self.db = Db()
        #print self.db

    def __set__(self, key, value):
        pass

    def __get__(self, instance, owner):
        pass


