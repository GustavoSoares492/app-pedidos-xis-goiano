from flask import Blueprint, redirect, render_template, request, url_for

from . import db, pedidos
from .models import Pedido, Produto

bp = Blueprint("main", __name__)


def _cardapio(erro=None, valores=None):
    return render_template(
        "cardapio.html", produtos=Produto.ativos(), erro=erro, valores=valores or {}
    )


def _endereco(itens, erros, dados):
    return render_template(
        "endereco.html",
        itens=itens,
        total=pedidos.total(itens),
        erros=erros,
        dados=dados,
    )


@bp.route("/saude")
def saude():
    return {"status": "ok"}


@bp.route("/")
def cardapio():
    return _cardapio()


@bp.route("/revisar", methods=["POST"])
def revisar():
    itens = pedidos.ler_itens(request.form)
    if not itens:
        return _cardapio(erro="Escolha pelo menos um item.", valores=request.form), 400
    return _endereco(itens, {}, {})


@bp.route("/pedido", methods=["POST"])
def registrar_pedido():
    itens = pedidos.ler_itens(request.form)
    if not itens:
        return _cardapio(erro="Escolha pelo menos um item.", valores=request.form), 400
    erros = pedidos.validar_entrega(request.form)
    if erros:
        return _endereco(itens, erros, request.form), 400
    pedido = pedidos.criar_pedido(request.form, itens)
    return redirect(url_for("main.confirmacao", pedido_id=pedido.id))


@bp.route("/pedido/<int:pedido_id>")
def confirmacao(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)
    return render_template("confirmacao.html", pedido=pedido)