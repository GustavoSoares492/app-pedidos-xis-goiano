from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.route("/saude")
def saude():
    return {"status": "ok"}