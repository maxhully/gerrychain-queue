from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping({"REDIS_CONFIG": get_redis_config(), "QUEUE_KEY": "queue"})

    from . import runs

    app.register_blueprint(runs.bp)

    from . import frontend

    app.register_blueprint(frontend.bp)

    return app


def get_redis_config():
    DEFAULT_CONFIG = {
        "REDIS_SERVICE_HOST": "redis",
        "REDIS_SERVICE_PORT": 6379,
        "REDIS_DB": 0,
        "REDIS_PASSWORD": None,
        "REDIS_SSL": False,
    }
    config = DEFAULT_CONFIG
    return {
        "host": config["REDIS_SERVICE_HOST"],
        "port": int(config["REDIS_SERVICE_PORT"]),
        "db": int(config["REDIS_DB"]),
        "password": config["REDIS_PASSWORD"],
        "ssl": bool(config["REDIS_SSL"]),
    }
