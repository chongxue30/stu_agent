from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.ai.chat_message import chat_message
from app.crud.ai.model import model
from app.crud.ai.api_key import api_key
from app.engine.model import ModelFactory
from app.services.chat.chat import get_session_history
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
import logging

logger = logging.getLogger(__name__)

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
            logger.error(f"模型 {model_id} 不存在")
            raise Exception("AI模型不存在")
        
        # 获取API密钥
        db_api_key = api_key.get(db, id=db_model.key_id)
        if not db_api_key:
            logger.error(f"API密钥 {db_model.key_id} 不存在")
            raise Exception("API密钥不存在")
        
        logger.info(f"使用模型 {db_model.name} ({db_model.platform}) 处理消息")
        
        # 构建上下文消息
        context_messages = []
        if use_context:
            context_messages = ChatService._build_context_messages(
                db, conversation_id, max_contexts
            )
            logger.info(f"加载了 {len(context_messages)} 条上下文消息")
        
        # 添加系统消息
        if system_message:
            context_messages.insert(0, {"role": "system", "content": system_message})
            logger.info("添加了系统消息")
        
        # 添加用户当前消息
        context_messages.append({"role": "user", "content": user_message})
        
        try:
            # 使用新的 ModelFactory 创建模型实例
            custom_config = {}
            if temperature is not None:
                custom_config["temperature"] = temperature
            if max_tokens is not None:
                custom_config["max_tokens"] = max_tokens

            logger.info(f"创建模型实例，自定义配置: {custom_config}")
            llm = ModelFactory.create_model_with_config(
                db=db,
                model_id=model_id,
                user_id=db_model.user_id,
                custom_config=custom_config or None
            )

            # 构建提示与链
            prompt_template = ChatPromptTemplate.from_messages([
                ('system', '你是一个乐于助人的助手。用{language}尽你所能回答所有问题。'),
                MessagesPlaceholder(variable_name='my_msg')
            ])
            chain = prompt_template | llm

            runnable = RunnableWithMessageHistory(
                chain,
                get_session_history,
                input_messages_key='my_msg'
            )

            config = {'configurable': {'session_id': str(conversation_id)}}
            response = runnable.invoke(
                {
                    'my_msg': [HumanMessage(content=user_message)],
                    'language': '中文'
                },
                config=config
            )

            return response.content
            
        except Exception as e:
            logger.error(f"AI模型调用失败: {str(e)}", exc_info=True)
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