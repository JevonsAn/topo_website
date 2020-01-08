# -*- coding: utf-8 -*-
import threading

from setting.db_query_setting import tablename_to_fields
from connection.mysql_conn import publicConnManage
from connection.redis_conn import redis_conn
import time
import json
import csv
from datetime import datetime
from datetime import date
from decimal import Decimal


class Echo(object):

    def write(self, value):
        return value


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def formatter(export_type, rows):
    def trans_list_to_xml(data_list):
        # 字典转换为xml字符串
        xml_data = []
        for row in data_list:
            xml_row = []
            for k in row.keys():  # 遍历字典排序后的key
                v = row.get(k)  # 取出字典中key对应的value
                xml_row.append(
                    '<{key}>{value}</{key}>'.format(key=k, value=v))
            xml_row = ''.join(xml_row)
            xml_row = '<row>{}</row>'.format(xml_row)
            xml_data.append(xml_row)
        xml_data = '<xml>{}</xml>'.format(''.join(xml_data))
        return xml_data

    def trans_list_to_csv(data_list):
        """A view that streams a large CSV file."""
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        first_line = sorted(data_list[0].keys())
        result = "\ufeff" + "".join([writer.writerow(first_line)] +
                                    [writer.writerow([row[k] for k in first_line]) for row in data_list])
        return result

    def trans_list_to_json(data_list):
        json_data = json.dumps(data_list, cls=CJsonEncoder, ensure_ascii=False, indent=4)
        return json_data

    if not rows:
        return ""

    if export_type == "csv":
        return trans_list_to_csv(rows)
    elif export_type == "json":
        return trans_list_to_json(rows)
    elif export_type == "xml":
        return trans_list_to_xml(rows)
    return ""


class Query(object):
    """
        此类功能：
        1.拼接sql语句
        2.通过mysql连接进行查询
    """

    def __init__(self, tablename, where_args, sort_args="", page_args="", export_args=""):
        self.tablename = tablename
        self.where_args = where_args
        sort_part = self.get_sort(sort_args)
        limit_part = self.get_page(page_args)
        where_part = self.get_where()
        self.where_part = where_part
        self.data_sql = "select * from " + tablename + where_part + sort_part + limit_part + ";"
        self.count_sql = "select count(*) as c from " + tablename + where_part + ";"
        self.export_sql = "select * from " + tablename + where_part + sort_part +limit_part+ ";"
        self.timeout_time = 1
        self.redis_tablename = "count_cache"
        self.key = self.tablename + "@" + self.where_part

    def get_where(self):
        tablename = self.tablename
        query = self.where_args
        if not tablename:
            return ""
        #此处and之后为检测为task的表
        if tablename not in tablename_to_fields and tablename.startswith("edges._"): 
            tablename = "odinary_task_table"

        fields = tablename_to_fields[tablename]["fields"]
        # print("fields:\n", fields)
        # sql_where = "where "
        in_conditions = []
        out_conditions = []
        others_conditions = []
        # print("进入get_where:")
        for key, value, joiner in query:
            # print("查询条件：", key, value, joiner)
            if key.find("in_out_") == 0:
                key = key[7:]
                # key = tablename_to_fields[table]["transform"].get(key, key)
                key = ("in_" + key, "out_" + key)
                # print(key)
                if (key[0] not in fields) or (key[1] not in fields):
                    # print("fields not exists this key：", key)
                    continue
                field = (fields[key[0]], fields[key[1]])

                if field[0]["type"] in {"varchar", "char"}:
                    in_conditions.append(key[0] + " " + joiner + " '" + value + "'")
                else:
                    in_conditions.append(key[0] + " " + joiner + " " + value + "")

                if field[1]["type"] in {"varchar", "char"}:
                    out_conditions.append(key[1] + " " + joiner + " '" + value + "'")
                else:
                    out_conditions.append(key[1] + " " + joiner + " " + value + "")
            else:
                # key = tablename_to_fields[table]["transform"].get(key, key)
                if key not in fields:
                    # print("fields not exists this key：", key)
                    others_conditions.append(key + " " + joiner + " " + value + "")
                    continue
                field = fields[key]
                if field["type"] in {"varchar", "char", "longtext"}:
                    others_conditions.append(key + " " + joiner + " '" + value + "'")
                else:
                    others_conditions.append(key + " " + joiner + " " + value + "")
            # where_conditions.append("")
        sql_where = self.__combination_where_condition(in_conditions, out_conditions, others_conditions)
        # print("sql_where:\n", sql_where)
        # print("拼接完成的条件：", sql_where)
        return sql_where

    def __combination_where_condition(self, in_conditions, out_conditions, others):
        sql_where = ' where '
        all_where = ''
        if in_conditions:
            in_where = " ( " + " and ".join(in_conditions) + " ) "
            all_where += in_where
        if out_conditions:
            out_where = " ( " + " and ".join(out_conditions) + " ) "
            if all_where:
                all_where += " or "
            all_where += out_where
        if others:
            other_where = " ( " + " and ".join(others) + " ) "
            if all_where:
                all_where = " ( " + all_where + " ) " + " and " + other_where
            else:
                all_where = other_where
        if all_where:
            sql_where += all_where
        else:
            sql_where = ''
        return sql_where

    def get_page(self, args):
        sql_limit = ""
        if args:
            sql_limit = " limit "
            sql_limit += str((int(args["pageIndex"]) - 1) * int(args["pageSize"])) + "," + str(args["pageSize"])
        return sql_limit

    def get_sort(self, sort_args):
        sort_part = ""
        if "sortField" in sort_args and "sortOrder" in sort_args:
            sort_part = " order by %s %s " % (
            sort_args["sortField"], "asc" if sort_args["sortOrder"] == "ascending" else "desc")
        return sort_part

    def fetch_count(self):
        result = redis_conn.hget(self.redis_tablename, self.key)
        if result:
            result = json.loads(result.decode())
        return result

    def exe_count(self):
        def exec_write_redis(this_object, outer_lock):
            outer_lock.acquire()
            start_time = time.time()
            rr = redis_conn.hset(this_object.redis_tablename, this_object.key,
                                 json.dumps({"itemsCount": None, "time": "未知"}))
            _, count_result = publicConnManage.execute_and_fetch(this_object.count_sql, use_pool=False, fetchone=True,
                                                                 dictionary=False)
            result = {
                "itemsCount": count_result[0],
                "time": time.time() - start_time
            }
            rr = redis_conn.hset(this_object.redis_tablename, this_object.key, json.dumps(result))
            try:
                outer_lock.release()
            except Exception as e:
                print(e)

        lock = threading.Lock()
        t = threading.Thread(target=exec_write_redis, args=(self, lock,))
        t.start()
        state = lock.acquire(blocking=True, timeout=self.timeout_time)  # 会阻塞

        del lock
        outer_result = self.fetch_count()
        return outer_result

    async def search(self):
        start = time.time()
        isSuccess, sql_result = publicConnManage.execute_and_fetch(self.data_sql)
        if not isSuccess:
            raise sql_result
        count_result = self.fetch_count()
        if count_result is None:
            count_result = self.exe_count()
        result = {
            "data": list(sql_result),
            "itemsCount": count_result["itemsCount"],
            "time": time.time() - start
        }
        return result

    async def searchCount(self):
        while not self.fetch_count():
            time.sleep(0.5)
        return self.fetch_count()

    async def searchExport(self):
        # print("============4=============")
        
        isSuccess, sql_result = publicConnManage.execute_and_fetch(self.export_sql, use_pool=False)
        # print("============5=============")
        if not isSuccess:
            raise sql_result
        return list(sql_result)

    async def searchBySQL(self, sql):
        """这个函数的sql参数中，暂不支持limit"""
        if not sql:
            return {}
        start = time.time()
        isSuccess, sql_result = publicConnManage.execute_and_fetch(sql)
        if not isSuccess:
            raise sql_result
        count_sql = "select count(*) as c from (%s) a" % sql.strip(";")  # 这条语句需要保证sql里没有limit
        isSuccess, count_result = publicConnManage.execute_and_fetch(count_sql, fetchone=True)
        if not isSuccess:
            raise count_result
        result = {
            "data": list(sql_result),
            "itemsCount": count_result["c"],
            "time": time.time() - start
        }
        return result
