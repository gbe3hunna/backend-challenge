from fastapi import APIRouter

from src.api.v1.routers import ecg, admin

router_v1 = APIRouter(prefix='/v1')

router_v1.include_router(admin.router)
router_v1.include_router(ecg.router)
