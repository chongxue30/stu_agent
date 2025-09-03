from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.ai.chat_message import chat_message
from app.crud.ai.chat_conversation import chat_conversation
from app.crud.ai.chat_role import chat_role
from app.crud.ai.model import model
from app.schemas.ai.chat_message import (
    ChatMessageCreate, ChatMessageUpdate, ChatMessagePageReq, ChatMessageSendReq, ChatMessageSendResp, ChatMessageResp
)
from app.schemas.common.response import PageResult, ResponseModel
from app.models.ai.chat_message import ChatMessage
from app.services.ai.chat import ChatService
import logging

logger = logging.getLogger(__name__)

class ChatMessageService:
    
    @staticmethod
    def send_message(db: Session, message_in: ChatMessageSendReq, user_id: int) -> ResponseModel[ChatMessageSendResp]:
        """发送消息并获取AI回复"""
        # 检查对话是否存在且属于当前用户
        db_conversation = chat_conversation.get(db, id=message_in.conversation_id)
        logger.info(f"处理会话ID {message_in.conversation_id} 的消息，用户ID: {user_id}")
        
        if not db_conversation:
            logger.error(f"会话 {message_in.conversation_id} 不存在")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在"
            )
        
        if db_conversation.user_id != user_id:
            logger.error(f"用户 {user_id} 无权访问会话 {message_in.conversation_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限在此对话中发送消息"
            )
        
        # 解析有效的角色与模型
        effective_role_id = message_in.role_id or db_conversation.role_id
        effective_system_message = db_conversation.system_message
        effective_model_id = db_conversation.model_id
        effective_model_str = db_conversation.model
        
        logger.info(f"初始配置 - 角色ID: {effective_role_id}, 模型ID: {effective_model_id}, 模型: {effective_model_str}")

        if effective_role_id:
            db_role = chat_role.get(db, id=effective_role_id)
            if db_role and not db_role.deleted:
                logger.info(f"使用角色 {db_role.name} (ID: {db_role.id}) 的配置")
                # 优先使用角色上的 system_message 与 model_id（如存在）
                if db_role.system_message:
                    effective_system_message = db_role.system_message
                    logger.info(f"使用角色的系统提示: {effective_system_message[:50]}...")
                if db_role.model_id:
                    effective_model_id = db_role.model_id
                    db_model = model.get(db, id=effective_model_id)
                    if db_model:
                        effective_model_str = db_model.model
                        logger.info(f"使用角色指定的模型: {effective_model_str} (ID: {effective_model_id})")

        logger.info(f"最终配置 - 角色ID: {effective_role_id}, 模型ID: {effective_model_id}, 模型: {effective_model_str}")

        # 创建用户消息
        user_msg = chat_message.create_user_message(
            db=db,
            conversation_id=message_in.conversation_id,
            user_id=user_id,
            content=message_in.content,
            model_id=effective_model_id,
            model=effective_model_str,
            role_id=effective_role_id
        )
        
        # 获取AI回复
        try:
            logger.info(f"开始调用AI模型 {effective_model_str} (ID: {effective_model_id})")
            ai_response = ChatService.get_ai_response(
                db=db,
                conversation_id=message_in.conversation_id,
                user_message=message_in.content,
                model_id=effective_model_id,
                system_message=effective_system_message,
                temperature=db_conversation.temperature,
                max_tokens=db_conversation.max_tokens,
                use_context=message_in.use_context,
                max_contexts=db_conversation.max_contexts
            )
            
            # 创建AI回复消息
            ai_msg = chat_message.create_ai_message(
                db=db,
                conversation_id=message_in.conversation_id,
                user_id=user_id,
                content=ai_response,
                model_id=effective_model_id,
                model=effective_model_str,
                reply_id=user_msg.id,
                role_id=effective_role_id
            )
            
            # 构建响应
            response = ChatMessageSendResp(
                message_id=ai_msg.id,
                content=ai_response,
                conversation_id=message_in.conversation_id,
                model=effective_model_str
            )
            
            return ResponseModel(data=response)
            
        except Exception as e:
            logger.error(f"AI回复失败: {str(e)}", exc_info=True)
            # 如果AI回复失败，删除用户消息
            chat_message.remove(db, id=user_msg.id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI回复失败: {str(e)}"
            )
    
    @staticmethod
    def get_message_list(db: Session, conversation_id: int, user_id: int, limit: int = 50) -> ResponseModel[List[ChatMessageResp]]:
        """获取对话的消息列表"""
        # 检查对话是否存在且属于当前用户
        db_conversation = chat_conversation.get(db, id=conversation_id)
        if not db_conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在"
            )
        
        if db_conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此对话"
            )
        
        messages = chat_message.get_by_conversation_id(db, conversation_id=conversation_id, limit=limit)
        return ResponseModel(data=[ChatMessageResp.model_validate(msg.to_dict()) for msg in messages])
    
    @staticmethod
    def delete_message(db: Session, id: int, user_id: int) -> ResponseModel[bool]:
        """删除消息"""
        db_message = chat_message.get(db, id=id)
        if not db_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="消息不存在"
            )
        
        if db_message.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此消息"
            )
        
        chat_message.soft_remove(db, id=id)
        return ResponseModel(data=True)
    
    @staticmethod
    def get_message_page(db: Session, page: ChatMessagePageReq, user_id: int) -> ResponseModel[PageResult[ChatMessageResp]]:
        """分页获取消息列表"""
        # 这里可以实现分页逻辑，暂时返回所有消息
        if page.conversation_id:
            messages = chat_message.get_by_conversation_id(db, conversation_id=page.conversation_id)
        else:
            messages = chat_message.get_by_user_id(db, user_id=user_id)
        
        # 应用过滤条件
        if page.type:
            messages = [m for m in messages if m.type == page.type]
        if page.user_id:
            messages = [m for m in messages if m.user_id == page.user_id]
        
        # 分页
        total = len(messages)
        start = (page.pageNo - 1) * page.pageSize
        end = start + page.pageSize
        page_messages = messages[start:end]
        
        page_result = PageResult(
            list=[ChatMessageResp.model_validate(msg.to_dict()) for msg in page_messages],
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        
        return ResponseModel(data=page_result)