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
import json

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
        
        # 构建最终的系统消息，包含模型身份
        model_identity_prompt = f"你是一个名为 {db_model.name} ({db_model.model}) 的AI助手，你的平台是 {db_model.platform}。你只应该自称 {db_model.name} ({db_model.model})，不要自称为DeepSeek或通义千问或任何其他平台/模型。"
        # 如果有自定义的 system_message，则将其追加到模型身份之后
        if system_message:
            final_system_prompt_content = model_identity_prompt + system_message
        else:
            final_system_prompt_content = model_identity_prompt
        final_system_prompt_content += f"用{{language}}尽你所能回答所有问题。"
        logger.info(f"最终系统提示: {final_system_prompt_content[:50]}...")
        
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
                ('system', final_system_prompt_content),
                MessagesPlaceholder(variable_name='chat_history'), # 放置对话历史
                ('human', '{human_input}') # 放置当前用户输入
            ])
            chain = prompt_template | llm

            runnable = RunnableWithMessageHistory(
                chain,
                input_messages_key='human_input', # 传递当前的用户输入
                history_messages_key='chat_history', # 告诉 RunnableWithMessageHistory 历史消息的占位符变量名
                get_session_history=lambda session_id: get_session_history(db, session_id, max_contexts) # 传递数据库会话和上下文限制
            )

            config = {'configurable': {'session_id': str(conversation_id)}}
            response = runnable.invoke({'human_input': user_message, 'language': '中文'},
                config=config
            )
            logger.info(f"模型原始回复: {response.content[:200]}...") # 打印模型原始回复

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
        
        # 构建最终的系统消息，包含模型身份
        model_identity_prompt = f"你是一个名为 {db_model.name} ({db_model.model}) 的AI助手，你的平台是 {db_model.platform}。你只应该自称 {db_model.name} ({db_model.model})，不要自称为DeepSeek或通义千问或任何其他平台/模型。"
        # 如果有自定义的 system_message，则将其追加到模型身份之后
        if system_message:
            final_system_prompt_content = model_identity_prompt + system_message
        else:
            final_system_prompt_content = model_identity_prompt
        final_system_prompt_content += f"用{{language}}尽你所能回答所有问题。"
        logger.info(f"最终系统提示 (流式): {final_system_prompt_content[:50]}...")

        # 构建上下文消息（流式需要自己构建，因为get_session_history是针对RunnableWithMessageHistory的）
        context_messages = []
        if use_context:
            context_messages = ChatService._build_context_messages(db, conversation_id, max_contexts)
            logger.info(f"加载了 {len(context_messages)} 条上下文消息 (流式)")
        
        # 添加系统消息到上下文，作为对话的第一条消息
        context_messages.insert(0, {"role": "system", "content": final_system_prompt_content})
        logger.info("添加了系统消息到上下文 (流式)")

        # 添加用户当前消息到上下文
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

            # 由于 stream_ai_response 不直接使用 RunnableWithMessageHistory，我们需要手动构建消息列表
            # 消息列表已经构建在 context_messages 中

            # 这里应该调用一个直接与LLM交互的函数，而不是chat_with_model，
            # chat_with_model 已经被重构为在 ChatService 中使用 LangChain 链。
            # 暂时，我们仍然假设 ModelFactory.create_model_with_config 返回的 llm 可以直接被 invoke。
            # 但是，llm.invoke 期望的是 LangChain 消息对象，不是字典列表。

            # 将 context_messages 转换为 LangChain 的消息格式
            from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
            langchain_messages = []
            for msg in context_messages:
                if msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))

            # 调用LLM进行流式生成
            response_generator = llm.stream(langchain_messages)
            full_response = ""
            for chunk in response_generator:
                full_response += chunk.content
                yield chunk.content
            logger.info(f"流式模型原始回复: {full_response[:200]}...") # 打印流式模型原始回复
            
            # stream_ai_response 的职责是返回流式内容，不应在此处创建消息或发送完成信号。
            # 消息创建和完成信号应由调用者 (e.g., chat_message.py 中的 send_message_stream) 处理。
            # 这里返回完整的响应内容，供调用者使用。
            return full_response
            
        except Exception as e:
            logger.error(f"AI模型流式调用失败: {str(e)}", exc_info=True)
            # 重新抛出异常，让调用者 (chat_message.py) 处理错误流
            raise Exception(f"AI模型流式调用失败: {str(e)}")