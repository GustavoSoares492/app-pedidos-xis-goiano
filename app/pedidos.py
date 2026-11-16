import re
from decimal import Decimal

from . import db
from .models import Cliente, ItemPedido, Pedido, Produto

QUANTIDADE_MAXIMA = 20

CAMPOS_OBRIGATORIOS = {
    "nome": "Informe o nome.",
    "telefone": "Informe o telefone com DDD.",
    "rua": "Informe a rua.",
    "numero": "Informe o número.",
    "bairro": "Informe o bairro.",
}


def ler_itens(form):
    """Lê quantidade e observação de cada produto ativo enviado no formulário."""
    itens = []
    for produto in Produto.ativos():
        try:
            quantidade = int(form.get(f"qtd_{produto.id}", "0") or 0)
        except ValueError:
            quantidade = 0
        quantidade = max(0, min(quantidade, QUANTIDADE_MAXIMA))
        if quantidade > 0:
            observacao = (form.get(f"obs_{produto.id}", "") or "").strip()[:200]
            itens.append(
                {"produto": produto, "quantidade": quantidade, "observacao": observacao}
            )
    return itens


def total(itens):
    return sum(
        (item["quantidade"] * item["produto"].preco for item in itens), Decimal("0.00")
    )


def validar_entrega(dados):
    """Devolve um dicionário {campo: mensagem}. Vazio quando está tudo certo."""
    erros = {}
    for campo, mensagem in CAMPOS_OBRIGATORIOS.items():
        if not (dados.get(campo) or "").strip():
            erros[campo] = mensagem
    if "telefone" not in erros:
        digitos = re.sub(r"\D", "", dados["telefone"])
        if len(digitos) not in (10, 11):
            erros["telefone"] = "Informe o telefone com DDD, por exemplo (62) 99999-9999."
    return erros


def criar_pedido(dados, itens):
    """Grava o cliente (reaproveitando o telefone), o pedido e os itens."""
    telefone = re.sub(r"\D", "", dados["telefone"])
    cliente = Cliente.query.filter_by(telefone=telefone).first()
    if cliente is None:
        cliente = Cliente(nome=dados["nome"].strip()[:100], telefone=telefone)
        db.session.add(cliente)

    pedido = Pedido(
        cliente=cliente,
        rua=dados["rua"].strip()[:120],
        numero=dados["numero"].strip()[:10],
        bairro=dados["bairro"].strip()[:80],
        referencia=(dados.get("referencia") or "").strip()[:120] or None,
    )
    for item in itens:
        pedido.itens.append(
            ItemPedido(
                produto=item["produto"],
                quantidade=item["quantidade"],
                preco_unitario=item["produto"].preco,
                observacao_item=item["observacao"] or None,
            )
        )
    db.session.add(pedido)
    db.session.commit()
    return pedido