from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.ai.chat_conversation import chat_conversation
from app.crud.ai.chat_role import chat_role
from app.crud.ai.model import model
from app.crud.ai.chat_message import chat_message
from app.schemas.ai.chat_conversation import (
    ChatConversationCreate, ChatConversationUpdate, ChatConversationPageReq, ChatConversationSimpleResp, ChatConversationResp
)
from app.schemas.common.response import PageResult, ResponseModel
from app.models.ai.chat_conversation import ChatConversation

class ChatConversationService:
    
    @staticmethod
    def create_conversation(db: Session, conversation_in: ChatConversationCreate, user_id: int) -> ResponseModel[int]:
        """创建聊天对话"""
        # 检查模型是否存在
        db_model = model.get(db, id=conversation_in.model_id)
        if not db_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI模型不存在"
            )
        
        # 检查角色是否存在（如果指定了角色）
        if conversation_in.role_id:
            db_role = chat_role.get(db, id=conversation_in.role_id)
            if not db_role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="聊天角色不存在"
                )
        
        # 创建对话
        conversation_data = conversation_in.dict()
        conversation_data["user_id"] = user_id
        conversation_data["creator"] = f"user_{user_id}"
        
        db_obj = chat_conversation.create(db, obj_in=conversation_data)
        return ResponseModel(data=db_obj.id)
    
    @staticmethod
    def update_conversation(db: Session, conversation_in: ChatConversationUpdate, user_id: int) -> ResponseModel[bool]:
        """更新聊天对话"""
        # 检查对话是否存在且属于当前用户
        db_conversation = chat_conversation.get(db, id=conversation_in.id)
        if not db_conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在"
            )
        
        if db_conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限操作此对话"
            )
        
        # 更新对话
        conversation_data = conversation_in.dict(exclude={"id"})
        conversation_data["updater"] = f"user_{user_id}"
        
        chat_conversation.update(db, db_obj=db_conversation, obj_in=conversation_data)
        return ResponseModel(data=True)
    
    @staticmethod
    def delete_conversation(db: Session, id: int, user_id: int) -> ResponseModel[bool]:
        """删除聊天对话"""
        result = chat_conversation.delete_by_user_id(db, id=id, user_id=user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在或无权限删除"
            )
        return ResponseModel(data=True)
    
    @staticmethod
    def get_conversation(db: Session, id: int, user_id: int) -> ResponseModel[ChatConversationResp]:
        """获取单个对话"""
        db_conversation = chat_conversation.get(db, id=id)
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
        
        return ResponseModel(data=ChatConversationResp.model_validate(db_conversation.to_dict()))
    
    @staticmethod
    def get_conversation_list(db: Session, user_id: int) -> ResponseModel[List[ChatConversationSimpleResp]]:
        """获取用户的对话列表"""
        conversations = chat_conversation.get_by_user_id(db, user_id=user_id)
        
        # 获取所有对话的ID
        conversation_ids = [conv.id for conv in conversations]
        # 获取消息数量映射
        message_counts = chat_message.get_message_count_by_conversation_ids(db, conversation_ids)
        
        conversation_resps = []
        for conv in conversations:
            conv_dict = conv.to_dict()
            conv_dict['messageCount'] = message_counts.get(conv.id, 0)
            conversation_resps.append(ChatConversationSimpleResp.model_validate(conv_dict))

        return ResponseModel(data=conversation_resps)
    
    @staticmethod
    def toggle_pin(db: Session, id: int, user_id: int) -> ResponseModel[bool]:
        """切换对话置顶状态"""
        conversation = chat_conversation.toggle_pin(db, id=id, user_id=user_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="对话不存在或无权限操作"
            )
        return ResponseModel(data=True)
    
    @staticmethod
    def get_conversation_page(db: Session, page: ChatConversationPageReq, user_id: int) -> ResponseModel[PageResult[ChatConversationResp]]:
        """分页获取对话列表"""
        # 这里可以实现分页逻辑，暂时返回所有对话
        conversations = chat_conversation.get_by_user_id(db, user_id=user_id)
        
        # 应用过滤条件
        if page.title:
            conversations = [c for c in conversations if page.title.lower() in c.title.lower()]
        if page.model_id:
            conversations = [c for c in conversations if c.model_id == page.model_id]
        if page.role_id:
            conversations = [c for c in conversations if c.role_id == page.role_id]
        if page.pinned is not None:
            conversations = [c for c in conversations if c.pinned == page.pinned]
        
        # 分页
        total = len(conversations)
        start = (page.pageNo - 1) * page.pageSize
        end = start + page.pageSize
        page_conversations = conversations[start:end]
        
        page_result = PageResult(
            list=[ChatConversationResp.model_validate(conv.to_dict()) for conv in page_conversations],
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        
        return ResponseModel(data=page_result)
