# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from datetime import datetime
from app.extensions import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))

    # Un cliente puede tener muchos pedidos
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)


class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    # Un producto puede estar en muchos pedidos
    pedidos = db.relationship('Pedido', backref='producto', lazy=True)


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    monto = db.Column(db.Float, nullable=False)
    # Cada pedido pertenece a un cliente y a un producto
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
