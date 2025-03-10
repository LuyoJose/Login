from fastapi.testclient import TestClient
from app import app  # Importa la app principal

client = TestClient(app)

def test_home_redirect_to_login():
    """Verifica que si no hay sesión, redirige a login"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Ingrese su usuario" in response.text  # Verifica que renderiza login.html

def test_register_user():
    """Verifica que un usuario puede registrarse correctamente"""
    response = client.post("/register", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 303  # Redirige a /
    assert "Location" in response.headers
    assert response.headers["Location"] == "/"

def test_register_existing_user():
    """Verifica que no se puedan registrar usuarios duplicados"""
    client.post("/register", data={"username": "testuser", "password": "testpass"})
    response = client.post("/register", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Usuario ya existe"}

def test_login_success():
    """Verifica el inicio de sesión exitoso"""
    client.post("/register", data={"username": "testuser", "password": "testpass"})
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 303  # Redirige a /
    assert response.headers["Location"] == "/"

def test_login_fail():
    """Verifica que no se pueda iniciar sesión con credenciales incorrectas"""
    response = client.post("/login", data={"username": "fakeuser", "password": "wrongpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Credenciales incorrectas"}

def test_logout():
    """Verifica que el usuario pueda cerrar sesión y sea redirigido al login"""
    client.post("/register", data={"username": "testuser", "password": "testpass"})
    client.post("/login", data={"username": "testuser", "password": "testpass"})
    response = client.get("/logout")
    assert response.status_code == 303
    assert response.headers["Location"] == "/"
