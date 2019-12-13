from abc import ABC

from tornado.web import RequestHandler
from setting.arg_setting import db_request_args, validate_args, db_required_args
from setting.db_query_setting import action_type_to_tablename, action_type_expire
from model.usual_query import Query, CJsonEncoder
import json


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
        self.write(json.dumps(query_result, ensure_ascii=False, indent=4, cls=CJsonEncoder))

    def on_finish(self):
        pass
