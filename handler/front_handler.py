from tornado.web import StaticFileHandler , HTTPError
class DefaultFileFallbackHandler(StaticFileHandler):
    def return400(self, reason):
        self.write(reason)
        self.set_status(400, "参数错误")
        self.finish()
    def prepare(self):
        self.args = {str(k): self.request.arguments[k][0].decode() for k in self.request.arguments}  # 获取所有参数
        # print(self.args)
        # self.return400("11")
    def validate_absolute_path(self, root, absolute_path):
        try:
            absolute_path = super().validate_absolute_path(root, absolute_path)
        except HTTPError:
            root = os.path.abspath(root)
            absolute_path = os.path.join(root, self.default_filename)
        return absolute_path