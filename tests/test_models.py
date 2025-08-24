import pytest
from models.client_model import Client
from database.db import SessionLocal

def test_client_model():
    """Test the Client model"""
    db = SessionLocal()
    
    # Create a new client
    client = Client(
        name="Test Client",
        type="Marketing",
        status="Active",
        settings="test settings"
    )
    
    db.add(client)
    db.commit()
    
    # Retrieve the client
    retrieved_client = db.query(Client).filter(Client.name == "Test Client").first()
    
    assert retrieved_client is not None
    assert retrieved_client.name == "Test Client"
    assert retrieved_client.type == "Marketing"
    assert retrieved_client.status == "Active"
    assert retrieved_client.visits == 0
    
    # Clean up
    db.delete(retrieved_client)
    db.commit()
    db.close()