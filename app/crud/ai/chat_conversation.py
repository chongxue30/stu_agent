from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.ai.chat_conversation import ChatConversation
from app.schemas.ai.chat_conversation import ChatConversationCreate, ChatConversationUpdate

class CRUDChatConversation(CRUDBase[ChatConversation, ChatConversationCreate, ChatConversationUpdate]):
    
    def get_by_user_id(self, db: Session, *, user_id: int) -> List[ChatConversation]:
        """根据用户ID获取对话列表"""
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.deleted == 0
        ).order_by(self.model.pinned.desc(), self.model.create_time.desc()).all()
    
    def get_by_user_id_and_model(self, db: Session, *, user_id: int, model_id: int) -> List[ChatConversation]:
        """根据用户ID和模型ID获取对话列表"""
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.model_id == model_id,
            self.model.deleted == 0
        ).order_by(self.model.create_time.desc()).all()
    
    def get_pinned_by_user_id(self, db: Session, *, user_id: int) -> List[ChatConversation]:
        """获取用户置顶的对话"""
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.pinned == 1,
            self.model.deleted == 0
        ).order_by(self.model.pinned_time.desc()).all()
    
    def toggle_pin(self, db: Session, *, id: int, user_id: int) -> Optional[ChatConversation]:
        """切换对话置顶状态"""
        conversation = db.query(self.model).filter(
            self.model.id == id,
            self.model.user_id == user_id,
            self.model.deleted == 0
        ).first()
        
        if conversation:
            conversation.pinned = not conversation.pinned
            if conversation.pinned:
                from sqlalchemy.sql import func
                conversation.pinned_time = func.now()
            else:
                conversation.pinned_time = None
            db.commit()
            db.refresh(conversation)
        
        return conversation
    
    def delete_by_user_id(self, db: Session, *, id: int, user_id: int) -> bool:
        """删除用户的对话（软删除）"""
        conversation = db.query(self.model).filter(
            self.model.id == id,
            self.model.user_id == user_id,
            self.model.deleted == 0
        ).first()
        
        if conversation:
            return self.soft_remove(db, id=id)
        return False

chat_conversation = CRUDChatConversation(ChatConversation)
