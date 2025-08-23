from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/modules")
async def list_modules(request: Request):
    modules = [
        {"name": "Content Studio", "description": "توليد محتوى نصي ومرئي", "active": True},
        {"name": "Sentiment Analyzer", "description": "تحليل المشاعر في النصوص", "active": True},
        {"name": "Social Sync Engine", "description": "نشر المحتوى على المنصات الاجتماعية", "active": True},
        {"name": "Performance Monitor", "description": "مراقبة أداء العملاء", "active": True},
        # أضف المزيد حسب الحاجة
    ]
    return templates.TemplateResponse("modules.html", {
        "request": request,
        "modules": modules
    })
