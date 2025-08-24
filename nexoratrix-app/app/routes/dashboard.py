from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Client
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    client_count = db.query(Client).count()
    active_modules = 4  # Example count of active modules
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "clients": clients,
        "client_count": client_count,
        "active_modules": active_modules
    })