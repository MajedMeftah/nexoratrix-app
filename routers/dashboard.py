from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import get_db
from models.client_model import Client

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    client_added: bool = Query(False),
    client_deleted: bool = Query(False)
):
    """
    لوحة التحكم الرئيسية - عرض إحصائيات العملاء والوحدات
    """
    clients = db.query(Client).all()
    client_count = db.query(Client).count()
    active_modules = 4  # Content Studio, Sentiment Analyzer, Social Sync, Performance Monitor
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "clients": clients,
            "client_count": client_count,
            "active_modules": active_modules,
            "client_added": client_added,
            "client_deleted": client_deleted
        }
    )
