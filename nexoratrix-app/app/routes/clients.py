from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.models import Client
from app.database import get_db
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/add-client")
def add_client(
    name: str = Form(...),
    type: str = Form(...),
    settings: str = Form(""),
    db: Session = Depends(get_db)
):
    client = Client(name=name, type=type, settings=settings)
    db.add(client)
    db.commit()
    return RedirectResponse("/dashboard?client_added=true", status_code=303)

@router.get("/client/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/edit-client/{client_id}")
def edit_client(client_id: int, name: str = Form(...), type: str = Form(...), settings: str = Form(""), db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        client.name = name
        client.type = type
        client.settings = settings
        db.commit()
        return RedirectResponse(f"/edit-client/{client_id}?updated=true", status_code=303)
    raise HTTPException(status_code=404, detail="Client not found")

@router.post("/delete-client/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
        return RedirectResponse("/dashboard?client_deleted=true", status_code=303)
    raise HTTPException(status_code=404, detail="Client not found")