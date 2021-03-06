import collections
import json

from flask import current_app, g
from redis import StrictRedis

from gerrychain_queue.models import Run


def get_queue():
    if "queue" not in g:
        g.queue = Queue(
            current_app.config["REDIS_CONFIG"],
            key=current_app.config["QUEUE_KEY"],
            Cache=StrictRedis,
        )
    return g.queue


class Queue:
    def __init__(self, redis_config, key="queue", Cache=StrictRedis, Task=Run):
        self.redis = Cache(**redis_config)
        self.Task = Task

        self.key = key
        self.statuses_key = key + "-statuses"

    def ping(self):
        return self.redis.ping()

    def list_tasks(self):
        statuses = {
            key.decode("utf-8"): value.decode("utf-8")
            for key, value in self.redis.hgetall(self.statuses_key).items()
        }
        tasks = [self.get_task(task_id).public() for task_id in statuses]
        for task in tasks:
            task["status"] = statuses[task["id"]]
        return tasks

    def add_task(self, task):
        task_json = json.dumps(task)

        self.update_status(task["id"], "WAITING")

        pipe = self.redis.pipeline()
        pipe.lpush(self.key, task_json)
        pipe.set(task["id"], task_json)
        pipe.execute()

    def get_task(self, task_id):
        task_json = self.redis.get(task_id)
        if task_json is None:
            raise KeyError
        return self.Task(json.loads(task_json))

    def get_status(self, task_id):
        status = self.redis.hget(self.statuses_key, task_id)
        if status is None:
            raise KeyError
        return status.decode("utf-8")

    def update_status(self, task_key, status):
        if status not in ("WAITING", "FAILED", "RUNNING", "COMPLETE"):
            raise ValueError(
                "Status is not one of 'WAITING', 'RUNNING', 'FAILED', or 'COMPLETE'"
            )
        self.redis.hset(self.statuses_key, task_key, status)
        self.send_message(task_key, "Status is set to {}".format(status))

    def send_message(self, task_key, message):
        self.redis.publish(channel=task_key, message=message)

    def get_report(self, task_key):
        elections = json.loads(
            self.redis.get(task_key + "-report").decode("utf-8").replace("'", '"')
        )
        for election in elections:
            for score in election["analysis"]:
                score["histogram"] = repair_histogram(score["histogram"])
        self.redis.set(task_key + "-report", json.dumps(elections))
        return elections


def repair_histogram(histogram):
    new_histogram = collections.defaultdict(int)
    for (left, right), count in histogram:
        new_histogram[(round(left, 4), round(right, 4))] += count
    return [((left, right), count) for (left, right), count in new_histogram.items()]
