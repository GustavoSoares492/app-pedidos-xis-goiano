from decimal import Decimal

from app import db
from app.models import Produto
from app.seed import semear_produtos


def baixar(client):
    resposta = client.get("/")
    return resposta, resposta.get_data(as_text=True)


def test_cardapio_responde_200(client):
    resposta, _ = baixar(client)
    assert resposta.status_code == 200


def test_cardapio_mostra_produto_ativo_com_preco_em_reais(client):
    db.session.add(Produto(nome="Xis Goiano", preco=Decimal("25.00")))
    db.session.commit()
    _, html = baixar(client)
    assert "Xis Goiano" in html
    assert "R$ 25,00" in html


def test_cardapio_esconde_produto_inativo(client):
    db.session.add(Produto(nome="Xis Antigo", preco=Decimal("20.00"), ativo=False))
    db.session.commit()
    _, html = baixar(client)
    assert "Xis Antigo" not in html


def test_cardapio_vazio_mostra_mensagem(client):
    _, html = baixar(client)
    assert "Nenhum produto disponível" in html


def test_seed_nao_duplica_produtos(app):
    assert semear_produtos() == 3
    assert semear_produtos() == 0
    assert Produto.query.count() == 3