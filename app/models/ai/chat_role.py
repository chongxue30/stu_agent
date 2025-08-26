from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ChatRole(Base):
    __tablename__ = "ai_chat_role"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="角色编号")
    user_id = Column(BigInteger, comment="用户编号")
    model_id = Column(BigInteger, ForeignKey("ai_model.id"), comment="模型编号")
    name = Column(String(128), nullable=False, comment="角色名称")
    avatar = Column(String(256), nullable=False, comment="头像")
    category = Column(String(32), comment="角色类别")
    sort = Column(Integer, nullable=False, default=0, comment="角色排序")
    description = Column(String(256), nullable=False, comment="角色描述")
    system_message = Column(String(1024), comment="角色上下文")
    knowledge_ids = Column(String(256), comment="关联的知识库编号数组")
    tool_ids = Column(String(256), comment="关联的工具编号数组")
    public_status = Column(Boolean, nullable=False, comment="是否公开")
    status = Column(Integer, comment="状态")
    
    # 通用字段
    creator = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updater = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(BigInteger, nullable=False, default=0, comment="租户编号")
    
    # 关联关系
    conversations = relationship("ChatConversation", foreign_keys="ChatConversation.role_id", back_populates="role")
    messages = relationship("ChatMessage", foreign_keys="ChatMessage.role_id", back_populates="role")
    ai_model = relationship("Model", foreign_keys=[model_id])
    
    def __repr__(self):
        return f"<ChatRole(id={self.id}, name='{self.name}', category='{self.category}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'model_id': self.model_id,
            'name': self.name,
            'avatar': self.avatar,
            'category': self.category,
            'sort': self.sort,
            'description': self.description,
            'system_message': self.system_message,
            'knowledge_ids': self.knowledge_ids,
            'tool_ids': self.tool_ids,
            'public_status': self.public_status,
            'status': self.status,
            'creator': self.creator,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'deleted': self.deleted,
            'tenant_id': self.tenant_id
        }
    
    @property
    def is_active(self):
        return self.status == 0 and not self.deleted
