from flask import Blueprint, render_template

bp = Blueprint("about", __name__, url_prefix="/about")


@bp.route("/")
def about():
    """
    Renders and returns the about page template.

    **Endpoint**: ``/about``
    """
    return render_template("about.html")
