import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database.db import get_db, Base

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

def test_home_page(client):
    """Test that the home page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "NexoraTrix" in response.text

def test_dashboard_page(client):
    """Test that the dashboard page loads correctly"""
    response = client.get("/dashboard")
    assert response.status_code == 200

def test_add_client(client):
    """Test adding a new client"""
    response = client.post("/add-client", data={
        "name": "Test Client",
        "type": "Marketing",
        "settings": ""
    })
    assert response.status_code == 303  # Redirect

def test_content_studio(client):
    """Test content studio module"""
    response = client.get("/content-studio")
    assert response.status_code == 200
    
    # Test content generation
    response = client.post("/content-studio", data={
        "prompt": "Test prompt"
    })
    assert response.status_code == 200
    assert "Test prompt" in response.text

def test_sentiment_analyzer(client):
    """Test sentiment analyzer module"""
    response = client.get("/sentiment-analyzer")
    assert response.status_code == 200
    
    # Test sentiment analysis
    response = client.post("/sentiment-analyzer", data={
        "text": "هذا نص جميل ورائع"
    })
    assert response.status_code == 200

def test_modules_page(client):
    """Test modules page"""
    response = client.get("/modules")
    assert response.status_code == 200

def test_about_page(client):
    """Test about page"""
    response = client.get("/about")
    assert response.status_code == 200

def test_roadmap_page(client):
    """Test roadmap page"""
    response = client.get("/roadmap")
    assert response.status_code == 200