# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Producto

bp_productos = Blueprint('productos', __name__, template_folder='templates')


def leer_formulario():
    """Devuelve (nombre, precio, stock) validados o None si hay error."""
    nombre = request.form['nombre'].strip()
    try:
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
    except ValueError:
        flash('El precio y el stock deben ser números.', 'danger')
        return None
    if not nombre or precio < 0 or stock < 0:
        flash('Completa el nombre; precio y stock no pueden ser negativos.', 'danger')
        return None
    return nombre, precio, stock


@bp_productos.route('/')
def lista():
    q = request.args.get('q', '').strip()
    consulta = Producto.query
    if q:
        consulta = consulta.filter(Producto.nombre.ilike('%' + q + '%'))
    productos = consulta.order_by(Producto.id).all()
    return render_template('productos/lista.html', productos=productos, q=q)


@bp_productos.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        datos = leer_formulario()
        if datos:
            nombre, precio, stock = datos
            db.session.add(Producto(nombre=nombre, precio=precio, stock=stock))
            db.session.commit()
            flash('Producto registrado correctamente.', 'success')
            return redirect(url_for('productos.lista'))
    return render_template('productos/form.html', producto=None)


@bp_productos.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    producto = db.get_or_404(Producto, id)
    if request.method == 'POST':
        datos = leer_formulario()
        if datos:
            producto.nombre, producto.precio, producto.stock = datos
            db.session.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('productos.lista'))
    return render_template('productos/form.html', producto=producto)


@bp_productos.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    producto = db.get_or_404(Producto, id)
    if producto.pedidos:
        flash('No se puede eliminar: el producto está en pedidos.', 'danger')
    else:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos.lista'))
