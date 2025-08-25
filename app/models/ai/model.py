from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Float
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.ai.api_key import ApiKey

class Model(Base):
    __tablename__ = "ai_model"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="编号")
    key_id = Column(BigInteger, ForeignKey("ai_api_key.id"), nullable=False, comment="API 秘钥编号")
    name = Column(String(64), nullable=False, comment="模型名字")
    model = Column(String(64), nullable=False, comment="模型标识")
    platform = Column(String(32), nullable=False, comment="模型平台")
    type = Column(Integer, nullable=False, comment="模型类型")
    sort = Column(Integer, nullable=False, comment="排序")
    status = Column(Integer, nullable=False, comment="状态")
    
    # 模型参数
    temperature = Column(Float, comment="温度参数")
    max_tokens = Column(Integer, comment="单条回复的最大 Token 数量")
    max_contexts = Column(Integer, comment="上下文的最大 Message 数量")
    
    # 关联关系
    api_key = relationship("ApiKey")
    
    # 通用字段
    creator = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updater = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(BigInteger, nullable=False, default=0, comment="租户编号")
