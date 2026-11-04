# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Cliente

bp_clientes = Blueprint('clientes', __name__, template_folder='templates')


@bp_clientes.route('/')
def lista():
    q = request.args.get('q', '').strip()
    consulta = Cliente.query
    if q:
        consulta = consulta.filter(Cliente.nombre.ilike('%' + q + '%'))
    clientes = consulta.order_by(Cliente.id).all()
    return render_template('clientes/lista.html', clientes=clientes, q=q)


@bp_clientes.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        telefono = request.form['telefono'].strip()
        if not nombre:
            flash('El nombre del cliente es obligatorio.', 'danger')
        else:
            db.session.add(Cliente(nombre=nombre, telefono=telefono))
            db.session.commit()
            flash('Cliente registrado correctamente.', 'success')
            return redirect(url_for('clientes.lista'))
    return render_template('clientes/form.html', cliente=None)


@bp_clientes.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    cliente = db.get_or_404(Cliente, id)
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        if not nombre:
            flash('El nombre del cliente es obligatorio.', 'danger')
        else:
            cliente.nombre = nombre
            cliente.telefono = request.form['telefono'].strip()
            db.session.commit()
            flash('Cliente actualizado correctamente.', 'success')
            return redirect(url_for('clientes.lista'))
    return render_template('clientes/form.html', cliente=cliente)


@bp_clientes.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    cliente = db.get_or_404(Cliente, id)
    if cliente.pedidos:
        flash('No se puede eliminar: el cliente tiene pedidos asociados.', 'danger')
    else:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes.lista'))
