from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Double, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ChatConversation(Base):
    __tablename__ = "ai_chat_conversation"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="对话编号")
    user_id = Column(BigInteger, nullable=False, comment="用户编号")
    role_id = Column(BigInteger, ForeignKey("ai_chat_role.id"), comment="聊天角色")
    title = Column(String(256), nullable=False, comment="对话标题")
    model_id = Column(BigInteger, ForeignKey("ai_model.id"), nullable=False, comment="模型编号")
    model = Column(String(32), nullable=False, comment="模型标识")
    pinned = Column(Boolean, nullable=False, comment="是否置顶")
    pinned_time = Column(DateTime, comment="置顶时间")
    system_message = Column(String(1024), comment="角色设定")
    temperature = Column(Double, nullable=False, comment="温度参数")
    max_tokens = Column(Integer, nullable=False, comment="单条回复的最大 Token 数量")
    max_contexts = Column(Integer, nullable=False, comment="上下文的最大 Message 数量")
    
    # 通用字段
    creator = Column(String(64), comment="创建人")
    create_time = Column(DateTime, comment="创建时间")
    updater = Column(String(64), comment="更新人")
    update_time = Column(DateTime, comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(BigInteger, comment="租户编号")
    
    # 关联关系
    messages = relationship("ChatMessage", foreign_keys="ChatMessage.conversation_id", back_populates="conversation")
    role = relationship("ChatRole", foreign_keys=[role_id])
    ai_model = relationship("Model", foreign_keys=[model_id])
    
    def __repr__(self):
        return f"<ChatConversation(id={self.id}, title='{self.title}', user_id={self.user_id})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'title': self.title,
            'model_id': self.model_id,
            'model': self.model,
            'pinned': self.pinned,
            'pinned_time': self.pinned_time.isoformat() if self.pinned_time else None,
            'system_message': self.system_message,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'max_contexts': self.max_contexts,
            'creator': self.creator,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'deleted': self.deleted,
            'tenant_id': self.tenant_id
        }
    
    @property
    def is_active(self):
        return not self.deleted
