from flask import Blueprint, render_template

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    """
    Renders and returns the template for the index page.

    **Endpoint**: ``/``
    """
    return render_template("index.html")
