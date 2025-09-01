from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Double, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

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
    messages = relationship("ChatMessage", back_populates="conversation", lazy="dynamic")
    role = relationship("ChatRole", foreign_keys=[role_id], lazy="joined")
    ai_model = relationship("Model", foreign_keys=[model_id], lazy="joined")
    
    def __repr__(self):
        return f"<ChatConversation(id={self.id}, title='{self.title}', user_id={self.user_id})>"
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': self.user_id,
            'title': self.title,
            'pinned': self.pinned,
            'role_id': self.role_id,
            'model_id': self.model_id,
            'model': self.model,
            'model_name': self.ai_model.name if self.ai_model else None,
            'system_message': self.system_message,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'max_contexts': self.max_contexts,
            'create_time': int(self.create_time.timestamp() * 1000) if self.create_time else None,
            'role_avatar': self.role.avatar if self.role else None,
            'role_name': self.role.name if self.role else None,
            'message_count': None, # 初始设置为 None，后续在 service 层填充
            'creator': self.creator,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'deleted': self.deleted,
            'tenant_id': self.tenant_id
        }
    
    @property
    def is_active(self):
        return not self.deleted
