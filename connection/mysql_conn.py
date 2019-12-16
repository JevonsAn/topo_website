#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector as mysql
from mysql.connector import pooling
from setting.database_setting import databases


class ConnManage(object):
    """一个mysql连接池   目前默认连接“edges”数据库
        提供查询功能，方便管理mysql连接
    """

    def __init__(self, pool_size=5):
        self.auth = {
            "host": databases["edges"]["host"],
            "user": databases["edges"]["user"],
            "passwd": databases["edges"]["passwd"],
            "db": databases["edges"]["db"],
            "port": databases["edges"]["port"],
        }
        self.pool = pooling.MySQLConnectionPool(pool_size=pool_size, pool_reset_session=True, **self.auth)

    def __del__(self):
        # self.pool.close() 没找到连接池关闭方式
        pass

    def _getConn(self, use_pool=True):
        if use_pool:
            return self.pool.get_connection()
        else:
            return mysql.connect(**self.auth)

    def execute_and_fetch(self, sql, fetchone=False, use_pool=True, dictionary=True):
        conn, cursor = None, None
        result = []
        try:
            conn = self._getConn(use_pool=use_pool)
            cursor = conn.cursor(dictionary=dictionary)
            print(sql)
            cursor.execute(sql)
            if fetchone:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        except Exception as e:
            return False, e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return True, result


publicConnManage = ConnManage()


class Mysql(object):
    def __init__(self, host="edges"):
        if host not in databases:
            raise ValueError("不存在的数据库")
        ip = databases[host]["host"]
        user = databases[host]["user"]
        passwd = databases[host]["passwd"]
        db = databases[host]["db"]
        port = databases[host]["port"]
        self.db = mysql.connect(host=ip, user=user, passwd=passwd, db=db, port=port)
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
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def __del__(self):
        self.close()
