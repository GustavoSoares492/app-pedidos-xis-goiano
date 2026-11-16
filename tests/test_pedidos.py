from decimal import Decimal

import pytest

from app import db, pedidos
from app.models import Cliente, Pedido, Produto

DADOS_OK = {
    "nome": "Cliente Teste",
    "telefone": "(62) 90000-0000",
    "rua": "Rua das Flores",
    "numero": "100",
    "bairro": "Centro",
}


def criar_produtos():
    xis = Produto(nome="Xis Goiano", preco=Decimal("25.00"))
    refri = Produto(nome="Refrigerante", preco=Decimal("6.00"))
    db.session.add_all([xis, refri])
    db.session.commit()
    return xis, refri


def test_validacao_aceita_dados_completos():
    assert pedidos.validar_entrega(DADOS_OK) == {}


@pytest.mark.parametrize("campo", ["nome", "telefone", "rua", "numero", "bairro"])
def test_validacao_exige_campos_obrigatorios(campo):
    dados = {**DADOS_OK, campo: "   "}
    assert campo in pedidos.validar_entrega(dados)


def test_validacao_recusa_telefone_curto():
    dados = {**DADOS_OK, "telefone": "12345"}
    assert "telefone" in pedidos.validar_entrega(dados)


def test_ler_itens_ignora_quantidade_zero_e_invalida(app):
    xis, refri = criar_produtos()
    form = {f"qtd_{xis.id}": "2", f"obs_{xis.id}": "sem cebola", f"qtd_{refri.id}": "abc"}
    itens = pedidos.ler_itens(form)
    assert len(itens) == 1
    assert itens[0]["quantidade"] == 2
    assert itens[0]["observacao"] == "sem cebola"


def test_ler_itens_limita_a_quantidade_maxima(app):
    xis, _ = criar_produtos()
    itens = pedidos.ler_itens({f"qtd_{xis.id}": "99"})
    assert itens[0]["quantidade"] == pedidos.QUANTIDADE_MAXIMA


def test_criar_pedido_grava_itens_e_total(app):
    xis, refri = criar_produtos()
    itens = pedidos.ler_itens({f"qtd_{xis.id}": "2", f"qtd_{refri.id}": "1"})
    pedido = pedidos.criar_pedido(DADOS_OK, itens)
    assert pedido.status == "recebido"
    assert pedido.total == Decimal("56.00")
    assert len(pedido.itens) == 2


def test_cliente_com_mesmo_telefone_e_reaproveitado(app):
    xis, _ = criar_produtos()
    itens = pedidos.ler_itens({f"qtd_{xis.id}": "1"})
    pedidos.criar_pedido(DADOS_OK, itens)
    pedidos.criar_pedido({**DADOS_OK, "telefone": "62 90000 0000"}, itens)
    assert Cliente.query.count() == 1
    assert Pedido.query.count() == 2