from flask import Blueprint, render_template

from .models import Produto

bp = Blueprint("main", __name__)


@bp.app_template_filter("brl")
def formatar_reais(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


@bp.route("/saude")
def saude():
    return {"status": "ok"}


@bp.route("/")
def cardapio():
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    return render_template("cardapio.html", produtos=produtos)