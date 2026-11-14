from decimal import Decimal

from . import db
from .models import Produto

# Preços fictícios: substituir pelos valores reais do cardápio da proprietária.
PRODUTOS_EXEMPLO = [
    ("Xis Goiano", "O xis gigante da casa, com queijo, presunto e salada", "25.00"),
    ("Batata frita (porção)", "Porção servida na cesta", "18.00"),
    ("Refrigerante", "Lata 350 ml", "6.00"),
]


def semear_produtos():
    """Cadastra os produtos de exemplo que ainda não existem. Devolve quantos criou."""
    criados = 0
    for nome, descricao, preco in PRODUTOS_EXEMPLO:
        if not Produto.query.filter_by(nome=nome).first():
            db.session.add(Produto(nome=nome, descricao=descricao, preco=Decimal(preco)))
            criados += 1
    db.session.commit()
    return criados