from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# قائمة الوحدات الذكية المتاحة في النظام
AVAILABLE_MODULES = [
    {
        "name": "Content Studio", 
        "description": "توليد محتوى نصي ومرئي", 
        "active": True,
        "manifest": "content_studio_manifest.yaml"
    },
    {
        "name": "Sentiment Analyzer", 
        "description": "تحليل المشاعر في النصوص", 
        "active": True,
        "manifest": "sentiment_analyzer_manifest.yaml"
    },
    {
        "name": "Social Sync Engine", 
        "description": "نشر المحتوى على المنصات الاجتماعية", 
        "active": True,
        "manifest": "social_sync_manifest.yaml"
    },
    {
        "name": "Performance Monitor", 
        "description": "مراقبة أداء العملاء", 
        "active": True,
        "manifest": "performance_monitor_manifest.yaml"
    },
]

@router.get("/modules", response_class=HTMLResponse)
async def list_modules(request: Request):
    """
    عرض قائمة جميع الوحدات الذكية المتاحة في النظام
    """
    return templates.TemplateResponse("modules.html", {
        "request": request,
        "modules": AVAILABLE_MODULES
    })

@router.get("/content-studio", response_class=HTMLResponse)
async def content_studio(request: Request):
    """
    وحدة توليد المحتوى (Content Studio)
    """
    return templates.TemplateResponse("content_studio.html", {
        "request": request, 
        "output": None
    })

@router.post("/content-studio", response_class=HTMLResponse)
async def generate_content(request: Request, prompt: str = Form(...)):
    """
    توليد محتوى جديد بناءً على المدخل المعطى
    """
    # نموذج توليد محتوى بسيط (بدون ذكاء اصطناعي حقيقي)
    output = f"محتوى مولّد بناءً على المدخل: {prompt}"
    return templates.TemplateResponse("content_studio.html", {
        "request": request, 
        "output": output, 
        "prompt": prompt
    })

@router.get("/sentiment-analyzer", response_class=HTMLResponse)
async def sentiment_analyzer(request: Request):
    """
    وحدة تحليل المشاعر (Sentiment Analyzer)
    """
    return templates.TemplateResponse("sentiment_analyzer.html", {
        "request": request, 
        "result": None, 
        "text": ""
    })

@router.post("/sentiment-analyzer", response_class=HTMLResponse)
async def analyze_sentiment(request: Request, text: str = Form(...)):
    """
    تحليل المشاعر في النص المعطى
    """
    # تحليل مشاعر بسيط جداً (تجريبي)
    positive_words = ["جيد", "ممتاز", "رائع", "جميل", "سعيد"]
    negative_words = ["سيء", "رديء", "حزين", "مزعج", "ضعيف"]
    
    score = 0
    for word in positive_words:
        if word in text:
            score += 1
    for word in negative_words:
        if word in text:
            score -= 1
    
    if score > 0:
        result = "إيجابي"
    elif score < 0:
        result = "سلبي"
    else:
        result = "محايد"
    
    return templates.TemplateResponse("sentiment_analyzer.html", {
        "request": request, 
        "result": result, 
        "text": text
    })

@router.get("/social-sync", response_class=HTMLResponse)
async def social_sync(request: Request):
    """
    وحدة مزامنة المنصات الاجتماعية (Social Sync Engine)
    """
    return templates.TemplateResponse("social_sync.html", {
        "request": request
    })

@router.get("/performance-monitor", response_class=HTMLResponse)
async def performance_monitor(request: Request):
    """
    وحدة مراقبة الأداء (Performance Monitor)
    """
    return templates.TemplateResponse("performance_monitor.html", {
        "request": request, 
        "client": None, 
        "visits": None
    })
