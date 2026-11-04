# TechBol - Segundo Parcial TEM-742 Tecnologias Emergentes II

Sistema monolitico modular para la gestion de inventario y ventas.
Flask (Application Factory + Blueprints), SQLAlchemy, Flask-Migrate y Bootstrap 5.

Autora: Milagros L. V. Bustamante Chuquimia (MLVBC) - RU 200091097 - UPEA

## Ejecutar
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    python -m flask --app run db upgrade
    python datos_prueba.py
    python run.py

Abrir http://127.0.0.1:5000

## Modulos
- /clientes (bp_clientes)
- /productos (bp_productos)
- /pedidos (bp_pedidos)
