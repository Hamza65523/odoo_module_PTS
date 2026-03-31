from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_auth, routes_device, routes_health, routes_pts, routes_status, routes_ws
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    stop_scheduler()


settings = get_settings()
app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api/v1"
app.include_router(routes_health.router)
app.include_router(routes_ws.router)
app.include_router(routes_auth.router, prefix=api_prefix)
app.include_router(routes_status.router, prefix=api_prefix)
app.include_router(routes_device.router, prefix=api_prefix)
app.include_router(routes_pts.router, prefix=api_prefix)
