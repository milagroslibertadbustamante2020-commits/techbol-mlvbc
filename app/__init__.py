# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Flask, render_template
from config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar los modelos para que las migraciones los detecten
    from app import models

    # Registro de los blueprints con sus prefijos
    from app.clientes.routes import bp_clientes
    from app.productos.routes import bp_productos
    from app.pedidos.routes import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix='/clientes')
    app.register_blueprint(bp_productos, url_prefix='/productos')
    app.register_blueprint(bp_pedidos, url_prefix='/pedidos')

    @app.route('/')
    def inicio():
        totales = {
            'clientes': models.Cliente.query.count(),
            'productos': models.Producto.query.count(),
            'pedidos': models.Pedido.query.count(),
        }
        return render_template('inicio.html', totales=totales)

    return app
