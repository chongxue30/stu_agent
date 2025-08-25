from fastapi import APIRouter
from app.api.v1.endpoints import auth  # 暂时注释掉 AI 路由

api_router = APIRouter()

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Support API"}

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["认证管理"])
# 暂时注释掉 AI 路由
# api_router.include_router(ai.router, prefix="/ai", tags=["AI 支持"])