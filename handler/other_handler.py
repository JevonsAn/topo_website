from abc import ABC

from tornado.web import RequestHandler
from setting.arg_setting import db_request_args, validate_args, db_required_args
from setting.db_query_setting import action_type_to_tablename, action_type_expire
from model.usual_query import Query, CJsonEncoder
from connection.mysql_conn import linkChangeConnManage
import json
import time

class OtherHandler(RequestHandler, ABC):
    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ('RETURN400',)

    def return400(self, reason):
        self.write(reason)
        self.set_status(400, "参数错误")
        self.finish()

    def prepare(self):
        self.args = {str(k): self.request.arguments[k][0].decode() for k in self.request.arguments}  # 获取所有参数
        print(self.args)
        # args = self.args
        # flag, msg = validate_args(args, db_required_args, db_request_args)
        # if not flag:
        #     self.return400(msg)

    async def get(self):
        args = self.args
        action = args["action"]
        typE = args["type"]
        sql = ""
        if action == "pop" and typE == "neighbor":
            if "pop_id" not in args or not args["pop_id"]:
                self.return400("缺少必要参数pop_id")
            pop_id = args.get("pop_id", "")
            sql = "(select n.pop_id as pop_id, n.geo as geo, n.num as num, e.num as num2 from " \
                  "edges.pop_node_table n, edges.pop_edge_table e where n.pop_id = e.in_pop_id and " \
                  "e.out_pop_id='%s') union " \
                  "(select n.pop_id as pop_id, n.geo as geo, n.num as num, e.num as num2 from edges.pop_node_table " \
                  "n, edges.pop_edge_table e where n.pop_id = e.out_pop_id and e.in_pop_id='%s');" \
                  % (pop_id, pop_id)

            query = Query("", "")
            query_result = await query.searchBySQL(sql)
        elif action == "link_change":
            def getTaskInfofromTablename(tablename):
                sp = tablename.split("_")
                size = len(sp)
                if size != 7:
                    return "", ""
                timestamp = sp[3]
                # print(sp, timestamp)
                return "N0700_" + timestamp + "_0000", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp[:-3])))
            
            starttime = time.time()
            isSuccess , tables = linkChangeConnManage.execute_and_fetch("select table_name from information_schema.tables where table_schema='edges' and table_type='base table' and table_name like '%N0700%';")
            if not isSuccess:
                raise tables
            results = []

            if typE == "edge":
                in_ip = args["in_ip"]
                out_ip = args["out_ip"]
                # print("=======================")
                # print(tables)
                # print("=======================")
                edge_table_names = [t["table_name"] for t in tables if t["table_name"].endswith("edge_table") and not t["table_name"].startswith("_parse")]
                for tablename in edge_table_names:
                    isSuccess , have_num = linkChangeConnManage.execute_and_fetch("select count(*) as c from %s where (in_ip, out_ip) in (('%s', '%s'), ('%s', '%s'));" % \
                        (tablename, in_ip, out_ip, out_ip, in_ip))
                    if not isSuccess:
                        raise have_num
                    # have_num=have_num[0]["c"]
                    if have_num[0]["c"]:
                        task_id, timestamp = getTaskInfofromTablename(tablename)
                        results.append({
                            "task_id": task_id,
                            "timestamp": timestamp
                        })
                isSuccess , r = linkChangeConnManage.execute_and_fetch("select first_seen, last_seen from edge_table where (in_ip, out_ip) = ('%s', '%s') limit 1" % (in_ip, out_ip))
                if not isSuccess:
                    raise r
                # r=r[0]
                first_seen = str(r[0]["first_seen"])
                last_seen = str(r[0]["last_seen"])
                if first_seen == last_seen:
                    results.append({
                        "task_id": "",
                        "timestamp": first_seen
                    })
                else:
                    results.append({
                        "task_id": "",
                        "timestamp": first_seen
                    })
                    results.append({
                        "task_id": "",
                        "timestamp": last_seen
                    })
            else:
                ip = args["ip"]
                node_table_names = [t["table_name"] for t in tables if t["table_name"].endswith("node_table") and not t["table_name"].startswith("_parse")]
                # print(node_table_names)
                for tablename in node_table_names:
                    isSuccess , have_num = linkChangeConnManage.execute_and_fetch("select count(*) as c from %s where ip='%s'" % (tablename, ip))
                    if not isSuccess:
                        raise r
                    have_num = have_num[0]["c"]
                    if have_num:
                        # print(tablename)
                        task_id, timestamp = getTaskInfofromTablename(tablename)
                        results.append({
                            "task_id": task_id,
                            "timestamp": timestamp
                        })
                isSuccess , r = linkChangeConnManage.execute_and_fetch("select first_seen, last_seen from node_table where ip='%s' limit 1" % (ip, ))
                if not isSuccess:
                    raise r
                # r = r[0]
                first_seen = str(r[0]["first_seen"])
                last_seen = str(r[0]["last_seen"])
                if first_seen == last_seen:
                    results.append({
                        "task_id": "",
                        "timestamp": first_seen
                    })
                else:
                    results.append({
                        "task_id": "",
                        "timestamp": first_seen
                    })
                    results.append({
                        "task_id": "",
                        "timestamp": last_seen
                    })
            query_result ={
                "data": results,
                "itemsCount": len(results),
                "time": time.time() - starttime
            }
        else:

            query = Query("", "")
            query_result = await query.searchBySQL(sql)
        self.write(json.dumps(query_result, ensure_ascii=False, indent=4, cls=CJsonEncoder))

    def on_finish(self):
        pass
