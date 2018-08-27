from uuid import uuid4

from flask import Blueprint, jsonify, abort

from gerrychain_queue.queue import get_queue

bp = Blueprint("runs", __name__, url_prefix="/runs")


@bp.route("/", methods=["POST"])
def create_run():
    task = {"id": uuid4().hex}
    q = get_queue()
    try:
        q.add_task(task)
    except Exception:
        abort(500)
    return jsonify(task)


@bp.route("/", methods=["GET"])
def list_runs():
    q = get_queue()
    tasks = q.list_tasks()
    return jsonify(tasks)


@bp.route("/<run_id>", methods=["GET"])
def get_run_details(run_id):
    q = get_queue()
    try:
        run_info = q.get_details(run_id)
    except KeyError:
        abort(404)
    return jsonify(run_info)
