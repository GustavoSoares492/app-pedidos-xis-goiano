from datetime import datetime, timezone
from decimal import Decimal

from . import db


def agora():
    return datetime.now(timezone.utc)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Numeric(8, 2), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False, unique=True)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=agora)
    pedidos = db.relationship("Pedido", back_populates="cliente")


class Pedido(db.Model):
    STATUS = ("recebido", "em preparo", "saiu para entrega", "entregue")

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    rua = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    bairro = db.Column(db.String(80), nullable=False)
    referencia = db.Column(db.String(120))
    observacoes = db.Column(db.String(300))
    status = db.Column(db.String(30), nullable=False, default="recebido")
    data_hora = db.Column(db.DateTime, nullable=False, default=agora)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    itens = db.relationship(
        "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
    )

    @property
    def total(self):
        return sum(
            (item.quantidade * item.preco_unitario for item in self.itens),
            Decimal("0.00"),
        )


class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(8, 2), nullable=False)
    observacao_item = db.Column(db.String(200))

    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto")