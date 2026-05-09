import pytest
from flask import Flask
import os
from routes import register_routes 
from models import db 

@pytest.fixture
def client():
    app = Flask(__name__)
    # Usamos SQLite en memoria para que el test sea ultra rápido
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    db.init_app(app) 
    
    with app.app_context():
        db.create_all() 
        register_routes(app)
        
    with app.test_client() as client:
        yield client

# TEST 10: Debe empezar por test_
def test_repuestos_bloqueo_sin_header(client):
    response = client.get('/api/repuestos')
    assert response.status_code == 403

# TEST 11: Debe empezar por test_
def test_repuestos_acceso_con_header(client):
    # Buscamos el token del .env o usamos el por defecto
    token = os.getenv('GATEWAY_INTERNAL_TOKEN', 'mi_token_secreto_123')
    response = client.get('/api/repuestos', headers={'X-Gateway-Secret': token})
    # Aquí debería dar 200 (OK) o 404 si la tabla está vacía, pero NO 403
    assert response.status_code != 403