import datetime
from abc import ABC

from tornado.web import RequestHandler
from setting.arg_setting import db_request_args, validate_args, db_required_args
from setting.db_query_setting import action_type_expire
from setting.task_query_setting import type_to_table_prefix
from model.usual_query import Query, CJsonEncoder, formatter
import json


class TaskHandler(RequestHandler, ABC):
    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ('RETURN400',)

    def return400(self, reason):
        self.write(reason)
        self.set_status(400, "参数错误")
        self.finish()

    def prepare(self):
        self.args = {str(k): self.request.arguments[k][0].decode() for k in self.request.arguments}  # 获取所有参数
        print(self.args)
        args = self.args
        flag, msg = validate_args(args, db_required_args, db_request_args)
        if not flag:
            self.return400(msg)

    async def get(self):
        args = self.args
        action = args["action"]
        typE = args["type"]
        if( "task_id" in args ):
            tablename = type_to_table_prefix[typE] + args["task_id"] + "_edge_table"
        else:
            tablename = "edges.edge_table"
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

    def on_finish(self):
        pass
