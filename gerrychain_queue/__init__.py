from flask import Flask

DEFAULT_CONFIG = {"REDIS_KEY": "gerrychain-queue"}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/hello")
    def hello():
        return "<h1>Hello, World!</h1>"

    return app
