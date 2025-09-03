from fastapi import APIRouter, HTTPException, Query
from app.services.ai_service import ai_support, chat_service, chat_with_deepseek_service, chat_with_zhipu_service

router = APIRouter()

# 自动生成SQL
@router.post("/generate-sql")
async def generate_sql_endpoint(question: str):
    try:
        # Call the ai_support function with the question parameter
        result = ai_support(question)
        return {"sql_query": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# 聊天机器人 - 支持模型选择
@router.post("/chat")
async def chat_endpoint(
    message: str, 
    session_id: str, 
    model_type: str = Query(default="zhipu", description="模型类型: zhipu")
):
    try:
        # 调用 chat_service 并传递 message、session_id 和 model_type
        result = chat_service(message, session_id, model_type)
        return {"response": result, "model_type": model_type}
    except HTTPException as e:
        raise e
    except Exception as e:
        # 捕获其他异常并返回 HTTP 错误
        raise HTTPException(status_code=500, detail=str(e))

# 兼容旧接口：DeepSeek 路由复用 zhipu 流程
@router.post("/chat/deepseek")
async def chat_deepseek_endpoint(message: str, session_id: str):
    try:
        result = chat_with_deepseek_service(message, session_id)
        return {"response": result, "model_type": "zhipu"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 专门使用智谱 AI 模型的聊天接口
@router.post("/chat/zhipu")
async def chat_zhipu_endpoint(message: str, session_id: str):
    try:
        result = chat_with_zhipu_service(message, session_id)
        return {"response": result, "model_type": "zhipu"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
