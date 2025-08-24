from fastapi import APIRouter

router = APIRouter()

from . import clients, dashboard, modules, settings

router.include_router(clients.router, prefix="/clients", tags=["clients"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(modules.router, prefix="/modules", tags=["modules"])
router.include_router(settings.router, prefix="/settings", tags=["settings"])