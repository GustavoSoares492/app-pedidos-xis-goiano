from decimal import Decimal

import pytest

from app import db
from app.models import Produto


@pytest.fixture
def xis(app):
    produto = Produto(nome="Xis Goiano", preco=Decimal("25.00"))
    db.session.add(produto)
    db.session.commit()
    return produto


def test_cardapio_mostra_passo_1_e_botao_com_destino(client, xis):
    html = client.get("/").get_data(as_text=True)
    assert "Passo 1 de 2" in html
    assert "Continuar para o endereço" in html


def test_endereco_mostra_passo_2_e_marca_campos_obrigatorios(client, xis):
    html = client.post("/revisar", data={f"qtd_{xis.id}": "1"}).get_data(as_text=True)
    assert "Passo 2 de 2" in html
    assert html.count('class="obrig"') == 5
    assert "Referência (opcional)" in html


def test_erro_vem_com_icone_e_foco_no_primeiro_campo(client, xis):
    dados = {
        f"qtd_{xis.id}": "1",
        "nome": "Cliente Teste",
        "telefone": "(62) 90000-0000",
        "rua": "Rua das Flores",
        "numero": "100",
        "bairro": "",
    }
    html = client.post("/pedido", data=dados).get_data(as_text=True)
    assert "Informe o bairro." in html
    assert "&#9888;" in html
    assert "primeiroErro.focus()" in html