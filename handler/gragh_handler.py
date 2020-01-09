from abc import ABC

from handler.BaseHandler import BaseHandler
from setting.arg_setting import validate_args, graph_request_args, graph_required_args
from model.graph_query import GraphQuery
from model.usual_query import CJsonEncoder
import json

graphQuery = GraphQuery()


class GraphHandler(BaseHandler, ABC):
    def prepare(self):
        self.args = {str(k): self.request.arguments[k][0].decode() for k in self.request.arguments}  # 获取所有参数
        print(self.args)
        args = self.args
        self.check_login_status()
        flag, msg = validate_args(args, graph_required_args, graph_request_args)
        if not flag:
            self.return400(msg)

    async def get(self):
        args = self.args
        action = args["action"]
        query_result = await graphQuery.search(action, args)
        self.write(json.dumps(query_result, ensure_ascii=False, indent=4, cls=CJsonEncoder))

    def on_finish(self):
        pass
