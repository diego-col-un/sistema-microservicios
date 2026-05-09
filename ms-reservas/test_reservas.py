from django.test import Client
import pytest
import os

# Test 14: Middleware de seguridad en Django
@pytest.mark.django_db
def test_django_security_middleware():
    client = Client()
    response = client.get('/api/reservas/')
    assert response.status_code == 403

# Test 15: Acceso exitoso con secreto en Django
@pytest.mark.django_db
def test_django_access_allowed():
    client = Client()
    token = os.getenv('GATEWAY_INTERNAL_TOKEN', 'mi_token_secreto_123')
    response = client.get('/api/reservas/', HTTP_X_GATEWAY_SECRET=token)
    assert response.status_code == 200