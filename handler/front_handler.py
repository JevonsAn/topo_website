from abc import ABC

from handler.BaseHandler import BaseHandler
from tornado.web import StaticFileHandler, HTTPError
from model.login import get_check_result
import os


class FileHandler(BaseHandler, ABC):
    async def prepare(self):
        self.args = {str(k): self.request.arguments[k][0].decode() for k in self.request.arguments}  # 获取所有参数
        print(self.args)
        self.check_login_status()

    async def get(self):
        self.render("../public/index.html")


class DefaultFileFallbackHandler(StaticFileHandler, ABC):
    def validate_absolute_path(self, root, absolute_path):
        try:
            absolute_path = super().validate_absolute_path(root, absolute_path)
        except HTTPError:
            root = os.path.abspath(root)
            absolute_path = os.path.join(root, self.default_filename)
        return absolute_path
