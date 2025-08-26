from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

class DictType(Base):
    __tablename__ = "system_dict_type"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="编号")
    name = Column(String(100), comment="字典名称")
    type = Column(String(100), comment="字典类型")
    status = Column(Integer, nullable=False, comment="状态")
    remark = Column(String(500), comment="备注")
    
    # 通用字段
    creator = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updater = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    deleted_time = Column(DateTime, comment="删除时间")
    
    def __repr__(self):
        return f"<DictType(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'remark': self.remark,
            'creator': self.creator,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'deleted': self.deleted,
            'deleted_time': self.deleted_time.isoformat() if self.deleted_time else None
        }
    
    @property
    def is_active(self):
        return self.status == 0 and not self.deleted
