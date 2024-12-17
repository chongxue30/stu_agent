from fastapi import APIRouter, HTTPException
from app.services.ai_service import ai_support
from app.services.ai_service import chat_service

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
    

# 聊天机器人
@router.post("/chat")
async def chat_endpoint(message: str, session_id: str):
    try:
        # 调用 chat_service 并传递 message 和 session_id
        result = chat_service(message, session_id)
        return {"response": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        # 捕获其他异常并返回 HTTP 错误
        raise HTTPException(status_code=500, detail=str(e))
