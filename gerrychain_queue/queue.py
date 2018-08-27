import json
from uuid import uuid4

from flask import current_app, g
from redis import StrictRedis


def get_queue():
    if "queue" not in g:
        g.queue = Queue(
            current_app.config["REDIS_CONFIG"], current_app.config["QUEUE_KEY"]
        )
    return g.queue


class Queue:
    def __init__(self, redis_config, key="queue"):
        self.redis = StrictRedis(**redis_config)
        self.key = key

    def ping(self):
        return self.redis.ping()

    def get_next_task(self):
        return self.redis.brpop(self.key)

    def list_tasks(self):
        json_items = self.redis.lrange(self.key, 0, -1)
        return [json.loads(item) for item in json_items]

    def get_details(self, task_id):
        details_json = self.redis.get(task_id)

        if details_json is None:
            raise KeyError

        print(details_json)

        details = json.loads(details_json)
        return details

    def update_status(self, task_key, message):
        self.redis.set(task_key, json.dumps({"id": task_key, "status": message}))

    def return_failed_task(self, task):
        task["attempts"] += 1
        self.redis.rpush(json.dumps(task))

    def add_task(self, task):
        if "id" not in task:
            task["id"] = uuid4().hex
        self.redis.lpush(self.key, json.dumps(task))
        self.update_status(task["id"], "Waiting...")
