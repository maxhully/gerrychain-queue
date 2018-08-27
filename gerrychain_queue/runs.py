from flask import Blueprint, jsonify, abort, request

from gerrychain_queue.queue import get_queue
from gerrychain_queue.models import Run

bp = Blueprint("runs", __name__, url_prefix="/runs")


@bp.route("/", methods=["POST"])
def create_run():
    try:
        run = Run(request.get_json())
    except ValueError as err:
        abort(400)

    document = run.public()
    q = get_queue()

    try:
        q.add_task(document)
    except Exception:
        abort(500)

    return jsonify(document)


@bp.route("/", methods=["GET"])
def list_runs():
    q = get_queue()
    tasks = q.list_tasks()
    return jsonify(tasks)


@bp.route("/<run_id>", methods=["GET"])
def get_run_status(run_id):
    q = get_queue()
    try:
        run_info = q.get_status(run_id)
    except KeyError:
        abort(404)
    return jsonify(run_info)
