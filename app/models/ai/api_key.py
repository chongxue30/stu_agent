from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.sql import func
from app.db.session import Base

class ApiKey(Base):
    __tablename__ = "ai_api_key"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="编号")
    name = Column(String(255), nullable=False, comment="名称")
    api_key = Column(String(1024), nullable=False, comment="密钥")
    platform = Column(String(255), nullable=False, comment="平台")
    url = Column(String(255), comment="自定义 API 地址")
    status = Column(Integer, nullable=False, comment="状态")
    
    # 通用字段
    creator = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updater = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(BigInteger, nullable=False, default=0, comment="租户编号")
