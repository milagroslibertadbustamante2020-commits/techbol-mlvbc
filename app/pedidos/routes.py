# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Pedido, Cliente, Producto

bp_pedidos = Blueprint('pedidos', __name__, template_folder='templates')


def leer_formulario():
    """Devuelve (cliente_id, producto_id, monto) o None si hay error."""
    try:
        cliente_id = int(request.form['cliente_id'])
        producto_id = int(request.form['producto_id'])
    except ValueError:
        flash('Selecciona un cliente y un producto.', 'danger')
        return None
    producto = db.session.get(Producto, producto_id)
    texto = request.form['monto'].strip()
    try:
        # Si el monto se deja vacío se usa el precio del producto
        monto = float(texto) if texto else producto.precio
    except ValueError:
        flash('El monto debe ser un número.', 'danger')
        return None
    if monto < 0:
        flash('El monto no puede ser negativo.', 'danger')
        return None
    return cliente_id, producto_id, monto


@bp_pedidos.route('/')
def lista():
    cliente_id = request.args.get('cliente_id', type=int)
    consulta = Pedido.query
    if cliente_id:
        consulta = consulta.filter_by(cliente_id=cliente_id)
    pedidos = consulta.order_by(Pedido.id.desc()).all()
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    total = sum(p.monto for p in pedidos)
    return render_template('pedidos/lista.html', pedidos=pedidos, clientes=clientes,
                           cliente_id=cliente_id, total=total)


@bp_pedidos.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    if not clientes or not productos:
        flash('Primero registra al menos un cliente y un producto.', 'warning')
        return redirect(url_for('pedidos.lista'))
    if request.method == 'POST':
        datos = leer_formulario()
        if datos:
            cliente_id, producto_id, monto = datos
            db.session.add(Pedido(cliente_id=cliente_id, producto_id=producto_id, monto=monto))
            db.session.commit()
            flash('Pedido registrado correctamente.', 'success')
            return redirect(url_for('pedidos.lista'))
    return render_template('pedidos/form.html', pedido=None, clientes=clientes, productos=productos)


@bp_pedidos.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    pedido = db.get_or_404(Pedido, id)
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    if request.method == 'POST':
        datos = leer_formulario()
        if datos:
            pedido.cliente_id, pedido.producto_id, pedido.monto = datos
            db.session.commit()
            flash('Pedido actualizado correctamente.', 'success')
            return redirect(url_for('pedidos.lista'))
    return render_template('pedidos/form.html', pedido=pedido, clientes=clientes, productos=productos)


@bp_pedidos.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    pedido = db.get_or_404(Pedido, id)
    db.session.delete(pedido)
    db.session.commit()
    flash('Pedido eliminado correctamente.', 'success')
    return redirect(url_for('pedidos.lista'))
