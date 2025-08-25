from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Common columns for all tables
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    creator = Column(String(64), nullable=True, default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updater = Column(String(64), nullable=True, default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    tenant_id = Column(Integer, nullable=False, default=0, comment="租户编号")
