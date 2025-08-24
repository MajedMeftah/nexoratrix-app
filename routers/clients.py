from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db import get_db
from models.client_model import Client
from models.client import Client as ClientSchema

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/clients", response_class=HTMLResponse)
async def list_clients(request: Request, db: Session = Depends(get_db)):
    """
    عرض قائمة جميع العملاء المسجلين في النظام
    """
    clients = db.query(Client).all()
    return templates.TemplateResponse("clients.html", {
        "request": request,
        "clients": clients
    })

@router.post("/clients")
async def add_client(
    name: str = Form(...),
    type: str = Form(...),
    settings: str = Form(""),
    db: Session = Depends(get_db)
):
    """
    إضافة عميل جديد إلى النظام
    """
    client = Client(name=name, type=type, settings=settings, status="Active")
    db.add(client)
    db.commit()
    return RedirectResponse("/dashboard?client_added=true", status_code=303)

@router.get("/clients/{client_id}", response_class=HTMLResponse)
async def get_client_details(client_id: int, request: Request, db: Session = Depends(get_db)):
    """
    عرض تفاصيل عميل معين مع الوحدات المرتبطة به
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return HTMLResponse("<h2>العميل غير موجود</h2>", status_code=404)
    
    # زيادة عدد الزيارات عند كل دخول للصفحة
    client.visits = (client.visits or 0) + 1
    db.commit()
    
    # Tabs لكل وحدة ذكية
    modules_tabs = [
        {"name": "Content Studio", "url": f"/content-studio?client_id={client_id}"},
        {"name": "Sentiment Analyzer", "url": f"/sentiment-analyzer?client_id={client_id}"},
        {"name": "Social Sync", "url": f"/social-sync?client_id={client_id}"},
        {"name": "Performance Monitor", "url": f"/performance-monitor?client_id={client_id}"}
    ]
    
    return templates.TemplateResponse("client_details.html", {
        "request": request, 
        "client": client, 
        "modules_tabs": modules_tabs
    })

@router.delete("/clients/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    حذف عميل من النظام
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return RedirectResponse("/dashboard?client_deleted=true", status_code=303)
