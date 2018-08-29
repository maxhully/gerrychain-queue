import json

from flask import current_app, g
from redis import StrictRedis

from gerrychain_queue.models import Run


def get_queue():
    if "queue" not in g:
        g.queue = Queue(
            current_app.config["REDIS_CONFIG"], current_app.config["QUEUE_KEY"]
        )
    return g.queue


class Queue:
    def __init__(self, redis_config, key="queue", Cache=StrictRedis):
        self.redis = Cache(**redis_config)
        self.key = key

    def ping(self):
        return self.redis.ping()

    def list_tasks(self):
        if self.redis.exists(self.key):
            json_items = self.redis.lrange(self.key, 0, -1)
            return [Run(json.loads(item)) for item in json_items]
        else:
            return []

    def get_status(self, task_id):
        status_json = self.redis.get(task_id)

        if status_json is None:
            raise KeyError

        status = json.loads(status_json)
        return status

    def update_status(self, task_key, message):
        self.redis.set(task_key, json.dumps({"id": task_key, "status": message}))

    def return_failed_task(self, task):
        task["attempts"] += 1
        self.redis.rpush(json.dumps(task))

    def add_task(self, task):
        self.redis.lpush(self.key, json.dumps(task))
        self.update_status(task["id"], "Waiting...")
