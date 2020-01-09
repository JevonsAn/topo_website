from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler
from handler.db_handler import DbHandler
from handler.gragh_handler import GraphHandler
from handler.other_handler import OtherHandler
from handler.task_handler import TaskHandler
from handler.front_handler import DefaultFileFallbackHandler, FileHandler


def make_app():
    return Application(
        [
            url(r"/db", DbHandler, name="db"),
            url(r"/graph", GraphHandler, name="graph"),
            url(r"/other", OtherHandler, name="other"),
            url(r"/getLinkChange", OtherHandler, name="getLinkChange"),
            url(r"/task_db", TaskHandler, name="task"),
            url(r'/', FileHandler),

            url(r'/static/(.*)', DefaultFileFallbackHandler,
                {
                    'path': 'public/static'
                }
                )
        ],
        debug=True
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(2525)
    IOLoop.current().start()
