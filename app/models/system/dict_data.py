from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

class DictData(Base):
    __tablename__ = "system_dict_data"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="编号")
    sort = Column(Integer, nullable=False, comment="排序")
    label = Column(String(100), comment="字典标签")
    value = Column(String(100), comment="字典键值")
    dict_type = Column(String(100), comment="字典类型")
    status = Column(Integer, nullable=False, comment="状态")
    color_type = Column(String(100), comment="颜色类型")
    css_class = Column(String(100), comment="CSS 样式")
    remark = Column(String(500), comment="备注")
    
    # 通用字段
    creator = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updater = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    deleted = Column(Boolean, nullable=False, default=False, comment="是否删除")
    
    def __repr__(self):
        return f"<DictData(id={self.id}, label='{self.label}', value='{self.value}', dict_type='{self.dict_type}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'sort': self.sort,
            'label': self.label,
            'value': self.value,
            'dict_type': self.dict_type,
            'status': self.status,
            'color_type': self.color_type,
            'css_class': self.css_class,
            'remark': self.remark,
            'creator': self.creator,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'deleted': self.deleted
        }
    
    @property
    def is_active(self):
        return self.status == 0 and not self.deleted
