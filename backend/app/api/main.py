from fastapi import APIRouter

from app.api.routes import login, employees, attendance

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
