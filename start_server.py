from tornado.ioloop import IOLoop
from tornado.web import Application, url
from handler.db_handler import DbHandler
from handler.gragh_handler import GraphHandler
from handler.other_handler import OtherHandler


def make_app():
    return Application(
        [
            url(r"/db", DbHandler, name="db"),
            url(r"/graph", GraphHandler, name="graph"),
            url(r"/other", OtherHandler, name="other"),
        ],
        debug=True
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(2525)
    IOLoop.current().start()
