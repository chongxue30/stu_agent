from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.ai.chat_message import chat_message
from app.crud.ai.model import model
from app.crud.ai.api_key import api_key
from app.services.chat.chat import chat_with_model

class ChatService:
    
    @staticmethod
    def get_ai_response(
        db: Session,
        conversation_id: int,
        user_message: str,
        model_id: int,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        use_context: bool = True,
        max_contexts: int = 10
    ) -> str:
        """获取AI回复"""
        # 获取模型信息
        db_model = model.get(db, id=model_id)
        if not db_model:
            raise Exception("AI模型不存在")
        
        # 获取API密钥
        db_api_key = api_key.get(db, id=db_model.key_id)
        if not db_api_key:
            raise Exception("API密钥不存在")
        
        # 构建上下文消息
        context_messages = []
        if use_context:
            context_messages = ChatService._build_context_messages(
                db, conversation_id, max_contexts
            )
        
        # 添加系统消息
        if system_message:
            context_messages.insert(0, {"role": "system", "content": system_message})
        
        # 添加用户当前消息
        context_messages.append({"role": "user", "content": user_message})
        
        try:
            # 调用AI模型
            # 这里需要根据平台选择不同的模型
            if db_model.platform.lower() == 'deepseek':
                response = chat_with_model(
                    message=user_message,
                    session_id=str(conversation_id),
                    language='中文',
                    model_type='deepseek',
                    api_key=db_api_key.api_key # 传递 API 密钥
                )
            else:
                response = chat_with_model(
                    message=user_message,
                    session_id=str(conversation_id),
                    language='中文',
                    model_type='zhipu',
                    api_key=db_api_key.api_key # 传递 API 密钥
                )
            
            return response
            
        except Exception as e:
            raise Exception(f"AI模型调用失败: {str(e)}")
    
    @staticmethod
    def _build_context_messages(db: Session, conversation_id: int, max_contexts: int) -> List[dict]:
        """构建上下文消息"""
        messages = chat_message.get_context_messages(db, conversation_id=conversation_id, max_contexts=max_contexts)
        
        context_messages = []
        for msg in reversed(messages):  # 反转顺序，从旧到新
            if msg.type == "user":
                context_messages.append({"role": "user", "content": msg.content})
            elif msg.type == "assistant":
                context_messages.append({"role": "assistant", "content": msg.content})
            elif msg.type == "system":
                context_messages.append({"role": "system", "content": msg.content})
        
        return context_messages
    
    @staticmethod
    def stream_ai_response(
        db: Session,
        conversation_id: int,
        user_message: str,
        model_id: int,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        use_context: bool = True,
        max_contexts: int = 10
    ):
        """流式获取AI回复（生成器）"""
        # 获取模型信息
        db_model = model.get(db, id=model_id)
        if not db_model:
            raise Exception("AI模型不存在")
        
        # 获取API密钥
        db_api_key = api_key.get(db, id=db_model.key_id)
        if not db_api_key:
            raise Exception("API密钥不存在")
        
        # 构建上下文消息
        context_messages = []
        if use_context:
            context_messages = ChatService._build_context_messages(
                db, conversation_id, max_contexts
            )
        
        # 添加系统消息
        if system_message:
            context_messages.insert(0, {"role": "system", "content": system_message})
        
        # 添加用户当前消息
        context_messages.append({"role": "user", "content": user_message})
        
        try:
            # 调用AI模型（流式）
            # 注意：当前的chat_with_model不支持流式，这里返回完整响应
            if db_model.platform.lower() == 'deepseek':
                response = chat_with_model(
                    message=user_message,
                    session_id=str(conversation_id),
                    language='中文',
                    model_type='deepseek',
                    api_key=db_api_key.api_key # 传递 API 密钥
                )
            else:
                response = chat_with_model(
                    message=user_message,
                    session_id=str(conversation_id),
                    language='中文',
                    model_type='zhipu',
                    api_key=db_api_key.api_key # 传递 API 密钥
                )
            
            # 模拟流式响应
            for i in range(0, len(response), 10):
                yield response[i:i+10]
                
        except Exception as e:
            yield f"错误: {str(e)}"
