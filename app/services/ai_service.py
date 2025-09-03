from app.services.chat.chat import chat_with_model, chat_with_zhipu
from fastapi import HTTPException
import traceback

def ai_support(question: str):
    """AI 支持服务"""
    try:
        # 这里可以添加具体的AI支持逻辑
        return f"AI 支持服务收到问题: {question}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def chat_service(message: str, session_id: str, model_type: str = 'zhipu'):
    """
    聊天服务，支持选择不同的模型
    
    Args:
        message: 用户消息
        session_id: 会话ID
        model_type: 模型类型 ('deepseek' 或 'zhipu')
    """
    try:
        # Ensure the message is of the correct type
        if not isinstance(message, str):
            raise ValueError("Input message must be a string.")
        
        # 根据模型类型选择对应的聊天函数（目前统一走 zhipu 风格）
        if model_type.lower() == 'zhipu':
            response = chat_with_zhipu(message, session_id)
            print(f"智谱 AI 聊天响应: {response}")
        else:
            # 默认使用 zhipu
            response = chat_with_model(message, session_id, model_type=model_type)
            print(f"默认模型聊天响应: {response}")
        
        return response
    except ValueError as ve:
        # Handle specific value errors
        print(f"ValueError in chat_service: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle general exceptions with detailed logging
        error_msg = f"Error during chat with {model_type}: {str(e)}"
        print(error_msg)
        print("Full traceback:")
        print(traceback.format_exc())
        
        # Return more specific error message
        if "API key" in str(e).lower() or "authentication" in str(e).lower():
            return "API 认证失败，请检查配置。"
        elif "connection" in str(e).lower() or "timeout" in str(e).lower():
            return "网络连接失败，请稍后重试。"
        else:
            return f"处理消息时发生错误: {str(e)}"

def chat_with_deepseek_service(message: str, session_id: str):
    """兼容旧接口：DeepSeek 路由暂时复用 zhipu 流程"""
    return chat_service(message, session_id, 'zhipu')

def chat_with_zhipu_service(message: str, session_id: str):
    """专门使用智谱 AI 模型的聊天服务"""
    return chat_service(message, session_id, 'zhipu')
