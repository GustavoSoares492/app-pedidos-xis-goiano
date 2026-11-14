# App de pedidos – Xis Goiano (MVP)

Aplicação web para receber e acompanhar pedidos de delivery do **Xis Goiano**, lanche familiar de Luziânia (GO).

## Problema
Hoje os pedidos chegam por WhatsApp e são digitados à mão em outro aplicativo. Essa dupla digitação causa erros de item e de endereço em todos os finais de semana, e o pedido precisa ser refeito.

## Solução (MVP)
- O cliente escolhe os itens e informa o endereço em um formulário com campos obrigatórios.
- A proprietária vê os pedidos recebidos em um painel único.
- Fora do escopo: pagamento online, integrações e atendimento de balcão.

## Tecnologias
Python 3.14, Flask, SQLite (Flask-SQLAlchemy) e pytest.

## ODS
ODS 8 – Trabalho Decente e Crescimento Econômico.

## Como rodar
```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

## Estrutura
- `app/` – código da aplicação
- `tests/` – testes automatizados

Projeto acadêmico – Experiência Prática 3, Projeto de Software.