from flask import Blueprint, render_template

from .models import Produto

bp = Blueprint("main", __name__)


@bp.route("/saude")
def saude():
    return {"status": "ok"}


@bp.route("/")
def cardapio():
    return render_template("cardapio.html", produtos=Produto.ativos())