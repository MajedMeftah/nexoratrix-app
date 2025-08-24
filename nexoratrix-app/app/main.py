from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import clients, dashboard, modules, settings

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(clients.router)
app.include_router(dashboard.router)
app.include_router(modules.router)
app.include_router(settings.router)

@app.get("/")
def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})