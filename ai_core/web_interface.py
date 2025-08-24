"""
واجهة الويب للمبرمج المستقل
Web Interface for Autonomous Programmer
"""

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
import uvicorn

from autonomous_programmer import AutonomousProgrammer

# إنشاء التطبيق
app = FastAPI(
    title="NexoraTrix AI Programmer",
    description="ذكاء اصطناعي متقدم للبرمجة المستقلة",
    version="2.0.0"
)

# إعداد القوالب والملفات الثابتة
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# إنشاء مثيل المبرمج
programmer = AutonomousProgrammer()

@app.on_event("startup")
async def startup_event():
    """بدء تشغيل النظام"""
    # بدء المبرمج في الخلفية
    asyncio.create_task(programmer.start())

@app.on_event("shutdown")
async def shutdown_event():
    """إيقاف النظام"""
    programmer.stop()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """الصفحة الرئيسية"""
    status = await programmer.get_status()
    return templates.TemplateResponse("ai_programmer_home.html", {
        "request": request,
        "status": status
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """لوحة التحكم"""
    status = await programmer.get_status()
    return templates.TemplateResponse("ai_programmer_dashboard.html", {
        "request": request,
        "status": status
    })

@app.post("/add-task")
async def add_task(
    description: str = Form(...),
    language: str = Form("python"),
    requirements: str = Form(""),
    complexity: str = Form("medium")
):
    """إضافة مهمة برمجية جديدة"""
    req_list = [req.strip() for req in requirements.split(",") if req.strip()]
    
    task_id = await programmer.add_task(
        description=description,
        language=language,
        requirements=req_list,
        complexity=complexity
    )
    
    return JSONResponse({
        "success": True,
        "task_id": task_id,
        "message": "تم إضافة المهمة بنجاح"
    })

@app.get("/api/status")
async def get_status():
    """API للحصول على حالة النظام"""
    status = await programmer.get_status()
    return JSONResponse(status)

@app.get("/api/tasks")
async def get_tasks():
    """API للحصول على قائمة المهام"""
    return JSONResponse({
        "tasks_in_queue": len(programmer.task_queue),
        "tasks": [
            {
                "task_id": task.task_id,
                "description": task.description,
                "language": task.language,
                "status": task.status
            }
            for task in programmer.task_queue
        ]
    })

@app.post("/api/learn")
async def trigger_learning(topic: str = Form(...)):
    """تشغيل التعلم حول موضوع معين"""
    try:
        learning_sessions = await programmer.internet_learner.search_and_learn(topic, max_results=5)
        return JSONResponse({
            "success": True,
            "sessions_count": len(learning_sessions),
            "message": f"تم التعلم حول {topic}"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)