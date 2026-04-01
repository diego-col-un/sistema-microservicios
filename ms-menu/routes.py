from flask import jsonify, request
from firebase_admin import db

def register_routes(app):

    # ─────────────────────────────────────────
    # GET /api/menu — listar todos los items
    # ─────────────────────────────────────────
    @app.route('/api/menu', methods=['GET'])
    def get_menu():
        ref   = db.reference('menu')
        items = ref.get()
        if not items:
            return jsonify({'success': True, 'data': []}), 200
        lista = [{'id': k, **v} for k, v in items.items()]
        return jsonify({'success': True, 'data': lista}), 200

    # ─────────────────────────────────────────
    # GET /api/menu/<id> — obtener uno
    # ─────────────────────────────────────────
    @app.route('/api/menu/<id>', methods=['GET'])
    def get_item(id):
        ref  = db.reference(f'menu/{id}')
        item = ref.get()
        if not item:
            return jsonify({'success': False, 'message': 'Item no encontrado'}), 404
        return jsonify({'success': True, 'data': {'id': id, **item}}), 200

    # ─────────────────────────────────────────
    # POST /api/menu — crear item
    # ─────────────────────────────────────────
    @app.route('/api/menu', methods=['POST'])
    def create_item():
        data = request.get_json()
        if not data or 'nombre' not in data or 'precio' not in data or 'categoria' not in data:
            return jsonify({'success': False, 'message': 'nombre, precio y categoria son requeridos'}), 400

        nuevo = {
            'nombre':       data['nombre'],
            'precio':       data['precio'],
            'categoria':    data['categoria'],
            'descripcion':  data.get('descripcion', ''),
            'disponible':   data.get('disponible', True),
            'imagen_url':   data.get('imagen_url', '')
        }

        ref      = db.reference('menu')
        nuevo_ref = ref.push(nuevo)
        return jsonify({'success': True, 'data': {'id': nuevo_ref.key, **nuevo}}), 201

    # ─────────────────────────────────────────
    # PUT /api/menu/<id> — actualizar item
    # ─────────────────────────────────────────
    @app.route('/api/menu/<id>', methods=['PUT'])
    def update_item(id):
        ref  = db.reference(f'menu/{id}')
        item = ref.get()
        if not item:
            return jsonify({'success': False, 'message': 'Item no encontrado'}), 404

        data = request.get_json()
        ref.update(data)
        updated = ref.get()
        return jsonify({'success': True, 'data': {'id': id, **updated}}), 200

    # ─────────────────────────────────────────
    # PUT /api/menu/<id>/disponibilidad — toggle disponible
    # ─────────────────────────────────────────
    @app.route('/api/menu/<id>/disponibilidad', methods=['PUT'])
    def toggle_disponibilidad(id):
        ref  = db.reference(f'menu/{id}')
        item = ref.get()
        if not item:
            return jsonify({'success': False, 'message': 'Item no encontrado'}), 404

        nuevo_estado = not item.get('disponible', True)
        ref.update({'disponible': nuevo_estado})
        return jsonify({
            'success':    True,
            'message':    f'Item {"disponible" if nuevo_estado else "no disponible"}',
            'disponible': nuevo_estado
        }), 200

    # ─────────────────────────────────────────
    # GET /api/menu/categoria/<categoria>
    # ─────────────────────────────────────────
    @app.route('/api/menu/categoria/<categoria>', methods=['GET'])
    def get_por_categoria(categoria):
        ref   = db.reference('menu')
        items = ref.get()
        if not items:
            return jsonify({'success': True, 'data': []}), 200
        filtrados = [
            {'id': k, **v} for k, v in items.items()
            if v.get('categoria') == categoria
        ]
        return jsonify({'success': True, 'data': filtrados}), 200

    # ─────────────────────────────────────────
    # DELETE /api/menu/<id> — eliminar item
    # ─────────────────────────────────────────
    @app.route('/api/menu/<id>', methods=['DELETE'])
    def delete_item(id):
        ref  = db.reference(f'menu/{id}')
        item = ref.get()
        if not item:
            return jsonify({'success': False, 'message': 'Item no encontrado'}), 404
        ref.delete()
        return jsonify({'success': True, 'message': 'Item eliminado'}), 200