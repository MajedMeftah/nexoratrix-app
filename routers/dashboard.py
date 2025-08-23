from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from database import get_client_count, get_module_count

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard(request: Request):
    client_count = get_client_count()
    module_count = get_module_count()
    # إضافة قائمة العملاء والوحدات النشطة للعرض في القالب إذا رغبت لاحقاً
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "client_count": client_count,
        "module_count": module_count
    })
