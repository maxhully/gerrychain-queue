from flask import Blueprint, render_template, request, redirect, url_for
from gerrychain_queue.runs import list_runs, create_run, get_run

bp = Blueprint("frontend", __name__, url_prefix="/")


@bp.route("/")
def home():
    runs = list_runs()
    return render_template("index.html", runs=runs)


@bp.route("/new")
def new():
    return render_template("new_slim.html")


@bp.route("/new/", methods=["POST"])
def post_new():
    run_spec = get_run_spec_from_form_data(request.form)
    document = create_run(run_spec)
    run_id = document["id"]
    return redirect(url_for("frontend.get_run_view", run_id=run_id))


def get_run_spec_from_form_data(form):
    run_spec = dict()
    run_spec["graph"] = "pa"
    run_spec["plan"] = form["plan"]
    run_spec["total_steps"] = int(form["steps"])
    return run_spec


@bp.route("/runs/<run_id>")
def get_run_view(run_id):
    return render_template("run_status.html", run=get_run(run_id))
