from flask_script import Command, Option
from gunicorn.app.base import Application
import multiprocessing


worker_count = 2 * multiprocessing.cpu_count() + 1


class GunicornServer(Command):

    description = "Run the app within Gunicorn"

    def __init__(self, host="127.0.0.1", port=8080, workers=worker_count, bind=None):
        self.port = port
        self.host = host
        self.workers = workers
        self.bind = bind

    def get_options(self):
        return (
            Option("-H", "--host", dest="host", default=self.host),
            Option("-p", "--port", dest="port", type=int, default=self.port),
            Option("-w", "--workers", dest="workers", type=int, default=self.workers),
            Option("-b", "--bind", dest="bind", default=None),
        )

    def handle(self, app, host, port, workers, bind):
        class FlaskApplication(Application):
            def init(self, parser, opts, args):
                if bind is None:
                    return {"bind": "{0}:{1}".format(host, port), "workers": workers}
                else:
                    return {"bind": bind, "workers": workers}

            def load(self):
                return app

        FlaskApplication().run()
