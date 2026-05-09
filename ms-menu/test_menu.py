import pytest
from unittest.mock import patch
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- TEST 12: Listar menú (GET /api/menu) ---
@patch('firebase_admin.db.reference')
def test_12_listar_menu(mock_db_ref, client):
    # Simulamos el formato exacto que devuelve Firebase .get() (un diccionario)
    menu_mock = {
        "-N12345": {"nombre": "Pizza", "precio": 25000, "categoria": "Cena"},
        "-N67890": {"nombre": "Jugo", "precio": 5000, "categoria": "Bebidas"}
    }
    mock_db_ref.return_value.get.return_value = menu_mock

    # ENVIAMOS EL TOKEN en los headers para saltar el middleware
    headers = {'X-Gateway-Secret': 'mi_token_secreto_123'}
    response = client.get('/api/menu', headers=headers)
    
    assert response.status_code == 200
    assert response.json['success'] is True
    # Verificamos que la lista tenga 2 items (el código los transforma de dict a lista)
    assert len(response.json['data']) == 2

# --- TEST 13: Obtener item por ID (GET /api/menu/:id) ---
@patch('firebase_admin.db.reference')
def test_13_obtener_item(mock_db_ref, client):
    item_especifico = {"nombre": "Pizza", "precio": 25000, "categoria": "Cena"}
    mock_db_ref.return_value.get.return_value = item_especifico

    headers = {'X-Gateway-Secret': 'mi_token_secreto_123'}
    # Probamos consultando el ID "-N12345"
    response = client.get('/api/menu/-N12345', headers=headers)

    assert response.status_code == 200
    assert response.json['data']['id'] == "-N12345"
    assert response.json['data']['nombre'] == "Pizza"