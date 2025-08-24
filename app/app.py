from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ai_support import router as ai_router
from app.database import engine, Base

# 创建 FastAPI 应用实例
app = FastAPI(
    title="AI Support API",
    description="AI 支持服务 API",
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
app.include_router(ai_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Support API"}
