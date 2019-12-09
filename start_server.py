from tornado.ioloop import IOLoop
from tornado.web import Application, url
from handler.db_handler import DbHandler


def make_app():
    return Application(
        [
            url(r"/db", DbHandler, name="db"),
        ],
        debug=True
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(2525)
    IOLoop.current().start()
