from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from models.client import Client

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# بيانات وهمية مؤقتة
clients = [
    Client(id=1, name="AlphaBot", type="Marketing", status="Active", settings="", visits=3),
    Client(id=2, name="LegalMind", type="Legal", status="Inactive", settings="", visits=1),
]

@router.get("/clients")
async def list_clients(request: Request):
    return templates.TemplateResponse("clients.html", {
        "request": request,
        "clients": clients
    })
