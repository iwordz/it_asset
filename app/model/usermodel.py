__author__ = 'fanghouguo'

from basemodel import basemodel


class usermodel(basemodel):
    db = None

    table = "auth_user"

    def __init__(self):
        super(usermodel, self).__init__()

    def count(self, where):
        return self.db.get_count(self.table, where)

    def insert(self, data):
        return self.db.insert(self.table, data)

    def update(self, value, where):
        return self.db.get_u_sql(self.table, value, where)

    def delete(self, where):
        return self.db.delete(self.table, where)

    def find(self, where):
        return self.db.find(self.table, where)
