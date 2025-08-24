from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "NexoraTrix" in response.text

def test_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Dashboard" in response.text

def test_add_client():
    response = client.post("/add-client", data={"name": "Test Client", "type": "Type A"})
    assert response.status_code == 303
    assert response.headers["location"] == "/?client_added=true"

def test_client_details():
    response = client.get("/client/1")
    assert response.status_code == 404  # Assuming no client with ID 1 exists

def test_performance_monitor():
    response = client.get("/performance-monitor")
    assert response.status_code == 200
    assert "Performance Monitor" in response.text

def test_settings_page():
    response = client.get("/settings")
    assert response.status_code == 200
    assert "Settings" in response.text

def test_contact_page():
    response = client.get("/contact")
    assert response.status_code == 200
    assert "Contact" in response.text

def test_about_page():
    response = client.get("/about")
    assert response.status_code == 200
    assert "About" in response.text

def test_roadmap_page():
    response = client.get("/roadmap")
    assert response.status_code == 200
    assert "Roadmap" in response.text

def test_logout_page():
    response = client.get("/logout")
    assert response.status_code == 200
    assert "Logout" in response.text