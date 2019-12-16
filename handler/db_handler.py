from abc import ABC

from tornado.web import RequestHandler
from setting.arg_setting import db_request_args, validate_args, db_required_args
from setting.db_query_setting import action_type_to_tablename, action_type_expire
from model.usual_query import Query, CJsonEncoder
import json


class DbHandler(RequestHandler, ABC):
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
        if not trans_args["export"]:
            query_result = await query.search()
            self.write(json.dumps(query_result, ensure_ascii=False, indent=4, cls=CJsonEncoder))
        else:
            self.write()

    def on_finish(self):
        pass
