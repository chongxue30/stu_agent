from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ai_support import router as ai_router
from app.routes.auth import router as auth_router
from app.database import engine, Base

app = FastAPI(
    title="AI Support API",
    description="AI 支持服务 API，包含用户认证和AI聊天功能",
    version="1.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 包含路由
app.include_router(auth_router)  # 认证路由
app.include_router(ai_router)    # AI 支持路由

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Support API"}

@app.get("/api-info")
async def get_api_info():
    """获取API信息"""
    return {
        "name": "AI Support API",
        "version": "1.0.0",
        "description": "AI 支持服务 API，包含用户认证和AI聊天功能",
        "endpoints": {
            "认证管理": "/auth",
            "AI 支持": "/ai-support",
            "健康检查": "/health"
        }
    }
