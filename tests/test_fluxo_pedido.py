from decimal import Decimal

import pytest

from app import db
from app.models import Pedido, Produto


@pytest.fixture
def produtos(app):
    xis = Produto(nome="Xis Goiano", preco=Decimal("25.00"))
    refri = Produto(nome="Refrigerante", preco=Decimal("6.00"))
    db.session.add_all([xis, refri])
    db.session.commit()
    return xis, refri


def formulario(produtos, **extras):
    xis, refri = produtos
    dados = {
        f"qtd_{xis.id}": "2",
        f"obs_{xis.id}": "sem cebola",
        f"qtd_{refri.id}": "1",
        "nome": "Cliente Teste",
        "telefone": "(62) 90000-0000",
        "rua": "Rua das Flores",
        "numero": "100",
        "bairro": "Centro",
        "referencia": "Próximo à praça",
    }
    dados.update(extras)
    return dados


def test_revisar_sem_itens_volta_ao_cardapio_com_mensagem(client, produtos):
    resposta = client.post("/revisar", data={})
    assert resposta.status_code == 400
    assert "Escolha pelo menos um item." in resposta.get_data(as_text=True)


def test_revisar_mostra_resumo_e_total(client, produtos):
    resposta = client.post("/revisar", data=formulario(produtos))
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "R$ 56,00" in html
    assert "sem cebola" in html
    assert 'name="bairro"' in html


def test_pedido_sem_bairro_nao_grava_e_mostra_erro_em_texto(client, produtos):
    resposta = client.post("/pedido", data=formulario(produtos, bairro=""))
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 400
    assert "Informe o bairro." in html
    assert "Rua das Flores" in html
    assert Pedido.query.count() == 0


def test_pedido_completo_grava_e_mostra_confirmacao(client, produtos):
    resposta = client.post(
        "/pedido", data=formulario(produtos), follow_redirects=True
    )
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "Pedido recebido" in html
    assert "R$ 56,00" in html
    pedido = Pedido.query.one()
    assert pedido.status == "recebido"
    assert pedido.bairro == "Centro"


def test_pedido_inexistente_retorna_404(client):
    assert client.get("/pedido/999").status_code == 404