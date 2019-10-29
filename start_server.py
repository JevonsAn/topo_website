from tornado.ioloop import IOLoop
from tornado.web import Application, url
from handler.db_handler import dbHandler


def make_app():
    return Application(
        [
            url(r"/db", dbHandler, name="db"),
        ],
        debug=True
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
