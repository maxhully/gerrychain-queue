import collections
import os

from flask import Flask

from .queue import Queue

DEFAULT_CONFIG = {"REDIS_KEY": "gerrychain-queue"}

app = Flask("gerrychain_queue")


@app.route("/")
def home():
    return "<h1>Hello</h1>"


def main():
    config = collections.ChainMap(os.environ, DEFAULT_CONFIG)
    queue = Queue(config["REDIS_URI"], config["REDIS_KEY"])
    return queue


if __name__ == "__main__":
    main()
