from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def modules_page(request: Request):
    return templates.TemplateResponse("modules.html", {"request": request})

@router.get("/content-studio", response_class=HTMLResponse)
def content_studio(request: Request):
    return templates.TemplateResponse("content_studio.html", {"request": request, "output": None})

@router.post("/content-studio", response_class=HTMLResponse)
def generate_content(request: Request, prompt: str = Form(...)):
    output = f"محتوى مولّد بناءً على المدخل: {prompt}"
    return templates.TemplateResponse("content_studio.html", {"request": request, "output": output, "prompt": prompt})

@router.get("/sentiment-analyzer", response_class=HTMLResponse)
def sentiment_analyzer(request: Request):
    return templates.TemplateResponse("sentiment_analyzer.html", {"request": request, "result": None, "text": ""})

@router.post("/sentiment-analyzer", response_class=HTMLResponse)
def analyze_sentiment(request: Request, text: str = Form(...)):
    positive_words = ["جيد", "ممتاز", "رائع", "جميل", "سعيد"]
    negative_words = ["سيء", "رديء", "حزين", "مزعج", "ضعيف"]
    score = 0
    for w in positive_words:
        if w in text:
            score += 1
    for w in negative_words:
        if w in text:
            score -= 1
    if score > 0:
        result = "إيجابي"
    elif score < 0:
        result = "سلبي"
    else:
        result = "محايد"
    return templates.TemplateResponse("sentiment_analyzer.html", {"request": request, "result": result, "text": text})

@router.get("/social-sync", response_class=HTMLResponse)
def social_sync(request: Request):
    return templates.TemplateResponse("social_sync.html", {"request": request, "result": None, "content": "", "platform": ""})

@router.post("/social-sync", response_class=HTMLResponse)
def sync_content(request: Request, content: str = Form(...), platform: str = Form(...)):
    result = f"تم نشر المحتوى على منصة {platform}: {content}"
    return templates.TemplateResponse("social_sync.html", {"request": request, "result": result, "content": content, "platform": platform})