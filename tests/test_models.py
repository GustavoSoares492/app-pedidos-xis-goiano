from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Cliente, ItemPedido, Pedido, Produto


def criar_pedido():
    cliente = Cliente(nome="Cliente Teste", telefone="(00) 90000-0000")
    xis = Produto(nome="Xis Goiano", preco=Decimal("25.00"))
    refri = Produto(nome="Refrigerante", preco=Decimal("6.00"))
    pedido = Pedido(
        cliente=cliente, rua="Rua das Flores", numero="100", bairro="Centro"
    )
    pedido.itens = [
        ItemPedido(produto=xis, quantidade=2, preco_unitario=xis.preco,
                   observacao_item="sem cebola"),
        ItemPedido(produto=refri, quantidade=1, preco_unitario=refri.preco),
    ]
    db.session.add(pedido)
    db.session.commit()
    return pedido


def test_produto_nasce_ativo_por_padrao(app):
    produto = Produto(nome="Batata frita", preco=Decimal("18.00"))
    db.session.add(produto)
    db.session.commit()
    assert produto.ativo is True


def test_pedido_nasce_com_status_recebido(app):
    pedido = criar_pedido()
    assert pedido.status == "recebido"


def test_total_do_pedido_soma_os_itens(app):
    pedido = criar_pedido()
    assert pedido.total == Decimal("56.00")


def test_item_guarda_o_preco_do_momento_da_compra(app):
    pedido = criar_pedido()
    produto = pedido.itens[0].produto
    produto.preco = Decimal("30.00")
    db.session.commit()
    assert pedido.total == Decimal("56.00")


def test_telefone_do_cliente_e_unico(app):
    db.session.add(Cliente(nome="Ana", telefone="(00) 91111-1111"))
    db.session.commit()
    db.session.add(Cliente(nome="Bia", telefone="(00) 91111-1111"))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_excluir_pedido_exclui_os_itens(app):
    pedido = criar_pedido()
    db.session.delete(pedido)
    db.session.commit()
    assert ItemPedido.query.count() == 0