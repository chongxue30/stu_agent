from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.system import dict_type, dict_data
from app.api.v1.ai import chat_conversation, chat_message, api_key, model, chat_role

api_router = APIRouter()

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Support API"}

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["认证管理"])

# 系统管理路由
api_router.include_router(dict_type.router, prefix="/system", tags=["系统管理"])
api_router.include_router(dict_data.router, prefix="/system", tags=["系统管理"])

# AI聊天路由
api_router.include_router(chat_conversation.router, prefix="/ai", tags=["AI聊天"])
api_router.include_router(chat_message.router, prefix="/ai", tags=["AI聊天"])

# AI管理路由
api_router.include_router(api_key.router, prefix="/ai", tags=["AI管理"])
api_router.include_router(model.router, prefix="/ai", tags=["AI管理"])
api_router.include_router(chat_role.router, prefix="/ai", tags=["AI管理"])