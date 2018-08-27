from flask import Flask

DEFAULT_CONFIG = {"REDIS_CONFIG": {"host": "localhost"}, "QUEUE_KEY": "queue"}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(**DEFAULT_CONFIG)

    from . import runs

    app.register_blueprint(runs.bp)

    from . import frontend

    app.register_blueprint(frontend.bp)

    return app
