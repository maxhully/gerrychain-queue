from flask import Blueprint, render_template
from gerrychain_queue.runs import list_runs

bp = Blueprint("frontend", __name__, url_prefix="/")


@bp.route("/")
def home():
    runs = list_runs()
    return render_template("index.html", runs=runs)


@bp.route("/new")
def create_run():
    return render_template("new.html")
