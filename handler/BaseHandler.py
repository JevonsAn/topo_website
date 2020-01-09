import datetime
from abc import ABC

from tornado.web import RequestHandler
from setting.arg_setting import db_request_args, validate_args, db_required_args
from model.login import get_check_result


class BaseHandler(RequestHandler, ABC):
    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ('RETURN400', 'RETURN_LOGIN_FAIL', 'CHECK_LOGIN_STATUS')

    def return400(self, reason):
        self.write(reason)
        self.set_status(400, "参数错误")

    def return_login_fail(self):
        self.render("../public/session_timeout.html")

    def check_login_status(self):
        userid = self.args.get('userid', "")
        username = self.args.get('username', "")
        token = self.args.get('token', "")
        if not (userid and username and token):
            userid = self.get_cookie('userid', "")
            username = self.get_cookie('username', "")
            token = self.get_cookie('token', "")
        self.login_info = (userid, username, token)

        # print(userid, username, token)
        check_status = get_check_result(userid, username, token)
        if not check_status:
            self.clear_cookie('token')
            self.clear_cookie('userid')
            self.clear_cookie('username')
            self.return_login_fail()

        if "userid" in self.args:
            del self.args["userid"]
        if "username" in self.args:
            del self.args["username"]
        if "token" in self.args:
            del self.args["token"]

        self.set_cookie('token', token, max_age=3600)
        self.set_cookie('userid', userid, max_age=3600)
        self.set_cookie('username', username, max_age=3600)
        return check_status

    async def prepare(self):
        # print(self.request.arguments)
        self.args = {str(k): self.request.arguments[k][0].decode() for k in self.request.arguments}  # 获取所有参数
        print(self.args)
        if self.check_login_status():
            flag, msg = validate_args(self.args, db_required_args, db_request_args)
            if not flag:
                self.return400(msg)
