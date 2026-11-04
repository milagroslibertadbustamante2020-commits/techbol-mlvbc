# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
# Carga datos de prueba en las tablas de TechBol (ejecutar una sola vez).
from app import create_app
from app.extensions import db
from app.models import Cliente, Producto, Pedido

app = create_app()

with app.app_context():
    if Producto.query.count() > 0:
        print('Ya existen datos de prueba. No se agregó nada.')
    else:
        productos = [
            Producto(nombre='Laptop Lenovo IdeaPad', precio=4500.00, stock=10),
            Producto(nombre='Mouse inalámbrico', precio=85.50, stock=40),
            Producto(nombre='Teclado mecánico', precio=320.00, stock=25),
            Producto(nombre='Monitor 24 pulgadas', precio=1200.00, stock=8),
            Producto(nombre='Memoria USB 64 GB', precio=60.00, stock=100),
        ]
        clientes = [
            Cliente(nombre='Carlos Mamani Quispe', telefono='71234567'),
            Cliente(nombre='Ana Flores Condori', telefono='76543210'),
            Cliente(nombre='Luis Choque Apaza', telefono='69988776'),
        ]
        db.session.add_all(productos + clientes)
        db.session.commit()

        pedidos = [
            Pedido(cliente_id=clientes[0].id, producto_id=productos[0].id, monto=productos[0].precio),
            Pedido(cliente_id=clientes[0].id, producto_id=productos[1].id, monto=productos[1].precio),
            Pedido(cliente_id=clientes[1].id, producto_id=productos[2].id, monto=productos[2].precio),
            Pedido(cliente_id=clientes[2].id, producto_id=productos[3].id, monto=productos[3].precio),
        ]
        db.session.add_all(pedidos)
        db.session.commit()
        print('Datos de prueba cargados: 5 productos, 3 clientes y 4 pedidos.')
