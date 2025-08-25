from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Text
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.ai.model import Model

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
    
    # 关联关系
    model = relationship("Model")
    
    # 通用字段
    creator = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updater = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(BigInteger, nullable=False, default=0, comment="租户编号")
