from flask import Blueprint, jsonify, abort, request, url_for

from gerrychain_queue.queue import get_queue
from gerrychain_queue.models import Run

bp = Blueprint("runs", __name__, url_prefix="/api/runs")


@bp.route("/", methods=["POST"])
def create_run_endpoint():
    run_spec = request.get_json()
    response = create_run(run_spec)
    return jsonify(response)


def create_run(run_spec):
    try:
        run = Run(run_spec)
    except ValueError as err:
        abort(400)

    document = run.public()
    q = get_queue()

    try:
        q.add_task(document)
    except Exception:
        abort(500)

    return document


@bp.route("/", methods=["GET"])
def list_runs_endpoint():
    return jsonify(list_runs())


def list_runs():
    q = get_queue()
    runs = q.list_tasks()
    inject_hrefs(runs)
    return runs


def inject_hrefs(resources):
    for resource in resources:
        resource["href"] = url_for("runs.get_run_endpoint", run_id=resource["id"])


@bp.route("/<run_id>", methods=["GET"])
def get_run_endpoint(run_id):
    return jsonify(get_run(run_id))


def get_run(run_id):
    q = get_queue()
    try:
        status = q.get_status(run_id)
        details = q.get_task(run_id)
    except KeyError:
        abort(404)
    run_info = details.public()
    run_info["status"] = status
    return run_info
