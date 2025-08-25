from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.ai import api_key, model, chat_role

def create_app() -> FastAPI:
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

    # Include routers
    app.include_router(api_key.router, prefix=f"{settings.API_V1_STR}/ai")
    app.include_router(model.router, prefix=f"{settings.API_V1_STR}/ai")
    app.include_router(chat_role.router, prefix=f"{settings.API_V1_STR}/ai")

    return app

app = create_app()
