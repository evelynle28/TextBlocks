import os
import sys
from PyQt5 import QtSql

def path_to_temp(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DbManager:
    def __init__(self, app_name):
        dir_path = path_to_temp('data')

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, app_name + '.db')

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(file_path)
        if not self.db.open():
            sys.exit(-1)

    def exec(self, statement):
        query = QtSql.QSqlQuery()
        query.exec(statement)

        return query
