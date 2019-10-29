#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector
from setting.database_setting import databases


class Mysql(object):
    def __init__(self, host="edges"):
        if host not in databases:
            raise ValueError("不存在的数据库")
        ip = databases[host]["host"]
        user = databases[host]["user"]
        passwd = databases[host]["passwd"]
        db = databases[host]["db"]
        port = databases[host]["port"]
        self.db = mysql.connector.connect(host=ip, user=user, passwd=passwd, db=db, port=port)
        self.cursor = self.db.cursor(dictionary=True)

    def exe(self, string, args=None):
        if args:
            self.cursor.execute(string, args)
        else:
            self.cursor.execute(string)

    def exemany(self, string, param):
        try:
            self.cursor.executemany(string, param)
        except Exception as e:
            print(e)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.db.close()
