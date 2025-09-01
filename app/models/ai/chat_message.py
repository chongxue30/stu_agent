from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
import json

class ChatMessage(Base):
    __tablename__ = "ai_chat_message"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="消息编号")
    conversation_id = Column(BigInteger, ForeignKey("ai_chat_conversation.id"), nullable=False, comment="对话编号")
    reply_id = Column(BigInteger, comment="回复编号")
    user_id = Column(BigInteger, nullable=False, comment="用户编号")
    role_id = Column(BigInteger, ForeignKey("ai_chat_role.id"), comment="角色编号")
    type = Column(String(16), nullable=False, comment="消息类型")
    model = Column(String(32), nullable=False, comment="模型标识")
    model_id = Column(BigInteger, ForeignKey("ai_model.id"), nullable=False, comment="模型编号")
    content = Column(Text, nullable=False, comment="消息内容")
    use_context = Column(Boolean, nullable=False, default=False, comment="是否携带上下文")
    segment_ids = Column(String(2048), comment="段落编号数组")
    
    # 通用字段
    creator = Column(String(64), comment="创建人")
    create_time = Column(DateTime, comment="创建时间")
    updater = Column(String(64), comment="更新人")
    update_time = Column(DateTime, comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(BigInteger, comment="租户编号")
    
    # 关联关系
    conversation = relationship("ChatConversation", back_populates="messages", lazy="joined")
    role = relationship("ChatRole", foreign_keys=[role_id], lazy="joined")
    ai_model = relationship("Model", foreign_keys=[model_id], lazy="joined")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, type='{self.type}', conversation_id={self.conversation_id})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'reply_id': self.reply_id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'type': self.type,
            'model': self.model,
            'model_id': self.model_id,
            'content': self.content,
            'use_context': self.use_context,
            'segment_ids': self.segment_ids,
            'creator': self.creator,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'deleted': self.deleted == b'\x01' if isinstance(self.deleted, bytes) else bool(self.deleted) if self.deleted is not None else False,
            'tenant_id': self.tenant_id
        }
    
    @property
    def segment_ids_list(self):
        """获取段落ID列表"""
        if self.segment_ids:
            try:
                return json.loads(self.segment_ids)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    @property
    def is_active(self):
        return not self.deleted
