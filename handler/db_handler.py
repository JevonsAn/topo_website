from tornado.web import RequestHandler
from setting.arg_setting import type_validate_functions, request_args, required_args
from setting.query_setting import action_type_to_tablename
from model.usual_query import Query
import json


class dbHandler(RequestHandler):
    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ('RETURN400',)

    def return400(self, reason):
        self.write(reason)
        self.set_status(400, "参数错误")
        self.finish()

    def prepare(self):
        args = self.request.arguments  # 获取所有参数
        # 验证必需参数是否存在
        for arg in required_args:
            if arg not in args:
                self.return400("必需参数 %s 不存在" % arg)
        # 验证每个参数是否合法
        for arg in args:
            if arg not in request_args:
                self.return400("参数 %s 不是合法参数" % arg)
            validate_func = type_validate_functions[request_args["arg"]["validate"]["type"]]
            value = self.get_argument(arg)
            extra_args = request_args["arg"]["validate"].get("args")
            result = False
            if not extra_args:
                result = validate_func(value, extra_args)
            else:
                result = validate_func(value)
            if not result:
                self.return400("参数 %s 的值不合法" % arg)

    async def get(self):
        args = self.request.arguments  # 获取所有参数
        action = args["action"]
        typE = args["type"]
        tablename = action_type_to_tablename[action][typE]
        trans_args = {}
        for arg in args:
            key_type = request_args[arg]["key_type"]
            if not key_type:
                continue
            if key_type not in trans_args:
                trans_args[key_type] = {arg: args[arg]}
            else:
                trans_args[key_type][arg] = args[arg]
        query = Query(tablename, trans_args["where"], trans_args["sort"], trans_args["page"], trans_args["export"])
        query_result = await query.search()
        self.write(json.dumps(query_result, ensure_ascii=False, indent=4))

    def on_finish(self):
        pass
