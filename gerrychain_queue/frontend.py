from flask import Blueprint, render_template, request, redirect, url_for
from gerrychain_queue.runs import list_runs
from gerrychain_queue.runs import create_run

bp = Blueprint("frontend", __name__, url_prefix="/")


@bp.route("/")
def home():
    runs = list_runs()
    return render_template("index.html", runs=runs)


@bp.route("/new")
def new():
    return render_template("new.html")


@bp.route("/new/", methods=["POST"])
def post_new():
    run_spec = get_run_spec_from_form_data(request.form)
    document = create_run(run_spec)
    run_id = document["id"]
    return redirect(url_for(".get_run_view", run_id=run_id))


def get_run_spec_from_form_data(form):
    run_spec = dict()
    run_spec["graph"] = "wisconsin"
    run_spec["constraints"] = resolve_constraints(form)
    run_spec["total_steps"] = form["steps"]
    return run_spec


def resolve_constraints(form):
    constraints = []
    if "compactness" in form["constraints"]:
        constraints.append(
            {
                "type": "compactness",
                "score": form["compactnessScore"],
                "tolerance": form["compactnessTolerance"],
            }
        )
    if "contiguous" in form["constraints"]:
        constraints.append("contiguous")
    if "population" in form["constraints"]:
        constraints.append(
            {"type": "population", "tolerance": form["populationTolerance"]}
        )
    return constraints


@bp.route("/runs/<run_id>")
def get_run_view(run_id):
    return redirect(url_for(".home"))
