from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api import api_router
import logging

def create_app() -> FastAPI:
    # 初始化日志级别
    logging.basicConfig(level=logging.INFO)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router (包含认证路由)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
