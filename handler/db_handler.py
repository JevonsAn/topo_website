import datetime
from abc import ABC

from handler.BaseHandler import BaseHandler
from setting.arg_setting import db_request_args, validate_args, db_required_args
from setting.db_query_setting import action_type_to_tablename, action_type_expire
from model.usual_query import Query, CJsonEncoder, formatter
from model.request import get_deviceinfos
import json


class DbHandler(BaseHandler, ABC):
    async def get(self):
        args = self.args
        action = args["action"]
        typE = args["type"]
        tablename = action_type_to_tablename[action][typE]

        count = False
        if "count" in args:
            count = True
            del args["count"]

        trans_args = {
            "where": [],
            "sort": {},
            "page": {},
            "export": {}
        }
        for arg in args:
            key_type = db_request_args[arg]["key_type"]
            if not key_type:
                continue
            if key_type == "where":
                joiner = db_request_args[arg]["joiner"]
                trans_args[key_type].append((arg, args[arg], joiner))  # 传入参数名、参数值、和查询连接符号
            else:
                trans_args[key_type][arg] = args[arg]

        if action in action_type_expire and typE in action_type_expire[action]:
            info = action_type_expire[action][typE]
            trans_args["where"].append((info["field"], info["value"], info["joiner"]))

        query = Query(tablename, trans_args["where"], trans_args["sort"], trans_args["page"], trans_args["export"])
        export_args = trans_args["export"]

        if (not export_args) or "export" not in export_args or "export_type" not in export_args:
            query_result = await query.search()

            # if typE == "node" and action in {"ipv4", "router", "gateway"}:
            #     iplist = []
            #     for i in query_result["data"]:
            #         iplist.append(i["ip"])
            #     try:
            #         deviceinfos = get_deviceinfos(iplist)
            #         for i, info in enumerate(deviceinfos):
            #             query_result["data"][i]["device_info"] = info
            #     except Exception as e:
            #         print("get_device_info error: ", e)

            self.write(json.dumps(query_result, ensure_ascii=False, indent=4, cls=CJsonEncoder))

        else:
            query_result = await query.searchExport()
            content = formatter(export_args["export_type"], query_result)
            type_map = {
                "json": "application/json",
                "xml": "application/xml",
                "csv": "text/csv"
            }
            self.set_header("Content-Disposition", "attachment;filename=%s.%s" %
                            (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), export_args["export_type"]))
            self.set_header("Content-Type", type_map[export_args["export_type"]])
            self.write(content)
