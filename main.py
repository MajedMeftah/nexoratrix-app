# NexoraTrix - النواة الأساسية (Core Engine)
# هذا الملف يمثل نقطة البداية لتطبيق FastAPI ويحتوي على صفحة رئيسية وروابط للوحدات الأساسية.
# المرحلة الحالية: Clean Architecture Implementation

from fastapi import FastAPI, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Import from our clean architecture structure
from database.db import get_db, engine, Base
from models import Client
from routers import clients, modules, dashboard

# إنشاء التطبيق
app = FastAPI(
    title="NexoraTrix",
    description="منصة ذكاء اصطناعي متعددة العملاء قابلة للتخصيص والتوسع",
    version="0.1.0"
)

# إعداد القوالب
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# إنشاء الجداول في قاعدة البيانات
from database.db import Base
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(clients.router, prefix="/api", tags=["clients"])
app.include_router(modules.router, prefix="/api", tags=["modules"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])

# إعدادات عامة للمنصة
platform_settings = {
    "name": "NexoraTrix",
    "main_color": "#4B00B5"
}

# الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    الصفحة الرئيسية - عرض ملخص وروابط للوحدات
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "platform_name": platform_settings["name"],
        "main_color": platform_settings["main_color"]
    })

# Dashboard (الطريق المباشر)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
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

# إدارة العملاء (الطرق المباشرة)
@app.post("/add-client")
def add_client(
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

@app.get("/client/{client_id}", response_class=HTMLResponse)
def client_details(client_id: int, request: Request, db: Session = Depends(get_db)):
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

@app.post("/delete-client/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    حذف عميل من النظام
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return RedirectResponse("/dashboard?client_deleted=true", status_code=303)

# الوحدات الذكية (الطرق المباشرة)
@app.get("/content-studio", response_class=HTMLResponse)
def content_studio(request: Request):
    """
    وحدة توليد المحتوى (Content Studio)
    """
    return templates.TemplateResponse("content_studio.html", {
        "request": request, 
        "output": None
    })

@app.post("/content-studio", response_class=HTMLResponse)
def generate_content(request: Request, prompt: str = Form(...)):
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

@app.get("/sentiment-analyzer", response_class=HTMLResponse)
def sentiment_analyzer(request: Request):
    """
    وحدة تحليل المشاعر (Sentiment Analyzer)
    """
    return templates.TemplateResponse("sentiment_analyzer.html", {
        "request": request, 
        "result": None, 
        "text": ""
    })

@app.post("/sentiment-analyzer", response_class=HTMLResponse)
def analyze_sentiment(request: Request, text: str = Form(...)):
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

@app.get("/social-sync", response_class=HTMLResponse)
def social_sync(request: Request):
    """
    وحدة مزامنة المنصات الاجتماعية (Social Sync Engine)
    """
    return templates.TemplateResponse("social_sync.html", {
        "request": request, 
        "result": None, 
        "content": "", 
        "platform": ""
    })

@app.post("/social-sync", response_class=HTMLResponse)
def sync_content(request: Request, content: str = Form(...), platform: str = Form(...)):
    """
    مزامنة المحتوى مع المنصات الاجتماعية
    """
    # محاكاة نشر المحتوى (بدون تكامل حقيقي)
    result = f"تم نشر المحتوى على منصة {platform}: {content}"
    return templates.TemplateResponse("social_sync.html", {
        "request": request, 
        "result": result, 
        "content": content, 
        "platform": platform
    })

@app.get("/performance-monitor", response_class=HTMLResponse)
def performance_monitor(request: Request):
    """
    وحدة مراقبة الأداء (Performance Monitor)
    """
    return templates.TemplateResponse("performance_monitor.html", {
        "request": request, 
        "client": None, 
        "visits": None
    })

@app.post("/performance-monitor", response_class=HTMLResponse)
def monitor_client(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    """
    مراقبة أداء عميل معين
    """
    client = db.query(Client).filter(Client.name == name).first()
    visits = client.visits if client else None
    return templates.TemplateResponse("performance_monitor.html", {
        "request": request, 
        "client": client, 
        "visits": visits
    })

# صفحات إضافية
@app.get("/stats", response_class=HTMLResponse)
def stats(request: Request, db: Session = Depends(get_db)):
    """
    صفحة الإحصائيات العامة
    """
    client_count = db.query(Client).count()
    active_modules = 4  # Content Studio, Sentiment Analyzer, Social Sync, Performance Monitor
    return templates.TemplateResponse("stats.html", {
        "request": request,
        "client_count": client_count,
        "active_modules": active_modules
    })

@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    """
    صفحة إعدادات المنصة
    """
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "name": platform_settings["name"],
        "main_color": platform_settings["main_color"],
        "saved": False
    })

@app.post("/settings", response_class=HTMLResponse)
def save_settings(request: Request, name: str = Form(...), main_color: str = Form(...)):
    """
    حفظ إعدادات المنصة
    """
    platform_settings["name"] = name
    platform_settings["main_color"] = main_color
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "name": name,
        "main_color": main_color,
        "saved": True
    })

