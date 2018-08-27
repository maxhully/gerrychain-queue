from flask import Flask
from .queue import get_queue

DEFAULT_CONFIG = {"REDIS_CONFIG": {"host": "localhost"}, "QUEUE_KEY": "queue"}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(**DEFAULT_CONFIG)

    @app.route("/hello")
    def hello():
        return "<h1>Hello, World!</h1>"

    @app.route("/redis")
    def ping_redis():
        q = get_queue()
        return str(q.ping())

    from . import runs

    app.register_blueprint(runs.bp)

    return app
