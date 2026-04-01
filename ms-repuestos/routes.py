from flask import jsonify, request
from models import Repuesto, db
from functools import wraps
import os

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Token {os.getenv('API_TOKEN', 'miclave123')}":
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated

def register_routes(app):

    # ─────────────────────────────────────────
    # GET /api/repuestos — listar todos
    # ─────────────────────────────────────────
    @app.route('/api/repuestos', methods=['GET'])
    def get_repuestos():
        repuestos = Repuesto.query.all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in repuestos]}), 200

    # ─────────────────────────────────────────
    # GET /api/repuestos/<id> — obtener uno
    # ─────────────────────────────────────────
    @app.route('/api/repuestos/<int:id>', methods=['GET'])
    def get_repuesto(id):
        repuesto = db.session.get(Repuesto, id)
        if not repuesto:
            return jsonify({'success': False, 'message': 'Repuesto no encontrado'}), 404
        return jsonify({'success': True, 'data': repuesto.to_dict()}), 200

    # ─────────────────────────────────────────
    # POST /api/repuestos — crear
    # ─────────────────────────────────────────
    @app.route('/api/repuestos', methods=['POST'])
    def create_repuesto():
        data = request.get_json()
        if not data or 'nombre' not in data or 'referencia' not in data or 'precio' not in data or 'marca' not in data:
            return jsonify({'success': False, 'message': 'nombre, referencia, marca y precio son requeridos'}), 400

        repuesto = Repuesto(
            nombre      = data['nombre'],
            referencia  = data['referencia'],
            marca       = data['marca'],
            precio      = data['precio'],
            stock       = data.get('stock', 0),
            stock_minimo = data.get('stock_minimo', 5),
            descripcion = data.get('descripcion', '')
        )
        db.session.add(repuesto)
        db.session.commit()
        return jsonify({'success': True, 'data': repuesto.to_dict()}), 201

    # ─────────────────────────────────────────
    # PUT /api/repuestos/<id> — actualizar
    # ─────────────────────────────────────────
    @app.route('/api/repuestos/<int:id>', methods=['PUT'])
    def update_repuesto(id):
        repuesto = db.session.get(Repuesto, id)
        if not repuesto:
            return jsonify({'success': False, 'message': 'Repuesto no encontrado'}), 404

        data = request.get_json()
        repuesto.nombre      = data.get('nombre',      repuesto.nombre)
        repuesto.referencia  = data.get('referencia',  repuesto.referencia)
        repuesto.marca       = data.get('marca',       repuesto.marca)
        repuesto.precio      = data.get('precio',      repuesto.precio)
        repuesto.stock       = data.get('stock',       repuesto.stock)
        repuesto.stock_minimo = data.get('stock_minimo', repuesto.stock_minimo)
        repuesto.descripcion = data.get('descripcion', repuesto.descripcion)
        db.session.commit()
        return jsonify({'success': True, 'data': repuesto.to_dict()}), 200

    # ─────────────────────────────────────────
    # PUT /api/repuestos/<id>/stock — actualizar stock
    # ─────────────────────────────────────────
    @app.route('/api/repuestos/<int:id>/stock', methods=['PUT'])
    def update_stock(id):
        repuesto = db.session.get(Repuesto, id)
        if not repuesto:
            return jsonify({'success': False, 'message': 'Repuesto no encontrado'}), 404

        data     = request.get_json()
        cantidad = data.get('cantidad', 0)
        tipo     = data.get('tipo', 'salida')

        if tipo == 'salida':
            if repuesto.stock < cantidad:
                return jsonify({'success': False, 'message': 'Stock insuficiente', 'stock_disponible': repuesto.stock}), 400
            repuesto.stock -= cantidad
        else:
            repuesto.stock += cantidad

        db.session.commit()
        return jsonify({'success': True, 'data': repuesto.to_dict()}), 200

    # ─────────────────────────────────────────
    # GET /api/repuestos/stock-bajo — stock bajo mínimo
    # ─────────────────────────────────────────
    @app.route('/api/repuestos/stock-bajo', methods=['GET'])
    def stock_bajo():
        repuestos = Repuesto.query.filter(Repuesto.stock <= Repuesto.stock_minimo).all()
        return jsonify({'success': True, 'data': [r.to_dict() for r in repuestos]}), 200

    # ─────────────────────────────────────────
    # DELETE /api/repuestos/<id> — eliminar
    # ─────────────────────────────────────────
    @app.route('/api/repuestos/<int:id>', methods=['DELETE'])
    def delete_repuesto(id):
        repuesto = db.session.get(Repuesto, id)
        if not repuesto:
            return jsonify({'success': False, 'message': 'Repuesto no encontrado'}), 404

        db.session.delete(repuesto)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Repuesto eliminado'}), 200