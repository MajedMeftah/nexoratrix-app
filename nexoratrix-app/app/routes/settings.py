from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

platform_settings = {
    "name": "NexoraTrix",
    "main_color": "#4B00B5"
}

@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "name": platform_settings["name"],
        "main_color": platform_settings["main_color"],
        "saved": False
    })

@router.post("/settings", response_class=HTMLResponse)
def save_settings(request: Request, name: str = Form(...), main_color: str = Form(...)):
    platform_settings["name"] = name
    platform_settings["main_color"] = main_color
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "name": name,
        "main_color": main_color,
        "saved": True
    })