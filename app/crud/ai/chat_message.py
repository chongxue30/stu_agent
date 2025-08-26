from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.ai.chat_message import ChatMessage
from app.schemas.ai.chat_message import ChatMessageCreate, ChatMessageUpdate

class CRUDChatMessage(CRUDBase[ChatMessage, ChatMessageCreate, ChatMessageUpdate]):
    
    def get_by_conversation_id(self, db: Session, *, conversation_id: int, limit: int = 50) -> List[ChatMessage]:
        """根据对话ID获取消息列表"""
        return db.query(self.model).filter(
            self.model.conversation_id == conversation_id,
            self.model.deleted == 0
        ).order_by(self.model.create_time.asc()).limit(limit).all()
    
    def get_context_messages(self, db: Session, *, conversation_id: int, max_contexts: int = 10) -> List[ChatMessage]:
        """获取对话的上下文消息"""
        return db.query(self.model).filter(
            self.model.conversation_id == conversation_id,
            self.model.deleted == 0
        ).order_by(self.model.create_time.desc()).limit(max_contexts).all()
    
    def get_by_user_id(self, db: Session, *, user_id: int) -> List[ChatMessage]:
        """根据用户ID获取消息列表"""
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.deleted == 0
        ).order_by(self.model.create_time.desc()).all()
    
    def get_latest_message(self, db: Session, *, conversation_id: int) -> Optional[ChatMessage]:
        """获取对话的最新消息"""
        return db.query(self.model).filter(
            self.model.conversation_id == conversation_id,
            self.model.deleted == 0
        ).order_by(self.model.create_time.desc()).first()
    
    def create_user_message(self, db: Session, *, conversation_id: int, user_id: int, 
                           content: str, model_id: int, model: str, role_id: Optional[int] = None) -> ChatMessage:
        """创建用户消息"""
        message_data = ChatMessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            type="user",
            model=model,
            model_id=model_id,
            content=content,
            role_id=role_id,
            use_context=True
        )
        return self.create(db, obj_in=message_data)
    
    def create_ai_message(self, db: Session, *, conversation_id: int, user_id: int,
                         content: str, model_id: int, model: str, reply_id: Optional[int] = None,
                         role_id: Optional[int] = None) -> ChatMessage:
        """创建AI回复消息"""
        message_data = ChatMessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            reply_id=reply_id,
            type="assistant",
            model=model,
            model_id=model_id,
            content=content,
            role_id=role_id,
            use_context=True
        )
        return self.create(db, obj_in=message_data)

chat_message = CRUDChatMessage(ChatMessage)
