# -*- coding: utf-8 -*-
from setting.db_query_setting import tablename_to_fields
from connection.mysql_conn import Mysql
import time
import json
import csv
from datetime import datetime
from datetime import date
from decimal import Decimal


def getCountryIpNum():
    conn = Mysql("statistics")
    conn.exe("select value_info from form_data where key_info = 'top_country_ip_num'; ")
    result = conn.fetchall()[0]["value_info"]
    return json.loads(result)


top_country_ipmap = getCountryIpNum()


class Echo(object):
    """
    An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
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


class Query(object):
    """
        此类功能：
        1.拼接sql语句
        2.通过mysql连接进行查询
    """

    def __init__(self, tablename, where_args, sort_args="", page_args="", export_args=""):
        sort_part = self.get_sort(sort_args)
        limit_part = self.get_page(page_args)
        where_part = self.get_where(tablename, where_args)
        self.tablename = tablename
        self.where_args = where_args
        self.data_sql = "select * from " + tablename + where_part + sort_part + limit_part + ";"
        self.count_sql = "select count(*) as c from " + tablename + where_part + sort_part + ";"

    def get_where(self, tablename, query):
        if not tablename:
            return ""
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
        return ""

    def export(self, query, rows):
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
            xml_data = '<xml>{}</xml>'.format(xml_data)
            return xml_data

        def trans_list_to_csv(data_list):
            """A view that streams a large CSV file."""
            # Generate a sequence of rows. The range is based on the maximum number of
            # rows that can be handled by a single sheet in most spreadsheet
            # applications.
            return data_list

        def trans_list_to_json(data_list):
            # print("data_list:")
            # print(data_list[:1])
            json_data = json.dumps(data_list, cls=CJsonEncoder, ensure_ascii=False, indent=4)
            return json_data

        t = time.time()

        if ("xml" == query["export_type"]):
            data = trans_list_to_xml(rows)
            response = FileResponse(data)
            response['Content-Type'] = 'application/xml'
            response['Content-Disposition'] = 'attachment;filename=' + \
                                              str(int(round(t * 1000000))) + '.xml'
        elif ("csv" == query["export_type"]):
            pseudo_buffer = Echo()
            # rows = (["Row {}".format(idx), str(idx)] for idx in xrange(65536))
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                             content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename=' + \
                                              str(int(round(t * 1000000))) + '.csv'
        # if("json" == query["export_type"]):
        else:
            data = trans_list_to_json(rows)
            response = FileResponse(data)
            response['Content-Type'] = 'application/json'
            response['Content-Disposition'] = 'attachment;filename=' + \
                                              str(int(round(t * 1000000))) + '.json'
        return response

    async def search(self):
        start = time.time()
        conn = Mysql("edges")
        print(self.data_sql)
        conn.exe(self.data_sql)
        sql_result = conn.fetchall()
        count_result = 0
        print(self.where_args)
        if self.tablename in {"edges.node_table", "edges.edge_table"} and len(self.where_args) == 1 and \
                self.where_args[0][1] in top_country_ipmap:
            count_result = top_country_ipmap[self.where_args[0][1]]
        # else:
        #     conn.exe(self.count_sql)
        #     count_result = conn.fetchall()[0]["c"]
        conn.close()
        result = {
            "data": list(sql_result),
            "itemsCount": count_result,
            "time": time.time() - start
        }
        return result
        # 这个地方可以再讨论，到底是返回response还是数据。
        # if("export" in http_args["export"] and http_args["export"]["export"] == "true"):
        #     # print("export is true")
        #     response = self.export(http_args["export"], result["data"])
        # else:
        #     response = HttpResponse(json.dumps(
        #         result, indent=4, cls=CJsonEncoder), content_type="application/json")
        # return response

    async def searchBySQL(self, sql):
        if not sql:
            return {}
        start = time.time()
        conn = Mysql("edges")
        print(sql)
        conn.exe(sql)
        sql_result = conn.fetchall()
        conn.exe("select count(*) as c from (%s) a" % sql.strip(";"))
        count_result = conn.fetchall()[0]["c"]
        conn.close()
        result = {
            "data": list(sql_result),
            "itemsCount": count_result,  # count_result[0]["count(*)"],
            "time": time.time() - start
        }
        return result
