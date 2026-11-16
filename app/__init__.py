import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///pedidos.db"),
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    from . import models  # noqa: F401  (registra as tabelas)
    from .formatos import formatar_reais
    from .routes import bp

    app.add_template_filter(formatar_reais, "brl")
    app.register_blueprint(bp)

    @app.cli.command("seed")
    def seed():
        """Cadastra os produtos de exemplo do cardápio."""
        from .seed import semear_produtos
        print(f"{semear_produtos()} produto(s) cadastrado(s).")

    with app.app_context():
        db.create_all()

    return app