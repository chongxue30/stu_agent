from sqlalchemy import Column, BigInteger, String, DateTime, Integer, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class SystemUser(Base):
    """系统用户模型"""
    __tablename__ = 'system_users'
    
    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    
    # 基本信息
    username = Column(String(30), nullable=False, unique=True, comment='用户账号')
    password = Column(String(100), nullable=False, default='', comment='密码')
    nickname = Column(String(30), nullable=False, comment='用户昵称')
    remark = Column(String(500), comment='备注')
    
    # 组织信息
    dept_id = Column(BigInteger, comment='部门ID')
    post_ids = Column(String(255), comment='岗位编号数组')
    
    # 联系信息
    email = Column(String(50), default='', comment='用户邮箱')
    mobile = Column(String(11), default='', comment='手机号码')
    
    # 个人信息
    sex = Column(Integer, default=0, comment='用户性别')
    avatar = Column(String(512), default='', comment='头像地址')
    
    # 状态信息
    status = Column(Integer, nullable=False, default=0, comment='帐号状态（0正常 1停用）')
    
    # 登录信息
    login_ip = Column(String(50), default='', comment='最后登录IP')
    login_date = Column(DateTime, comment='最后登录时间')
    
    # 审计信息
    creator = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, nullable=False, default=func.now(), comment='创建时间')
    updater = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    # 软删除
    deleted = Column(Boolean, nullable=False, default=False, comment='是否删除')
    
    # 租户信息
    tenant_id = Column(BigInteger, nullable=False, default=0, comment='租户编号')
    
    def __repr__(self):
        return f"<SystemUser(id={self.id}, username='{self.username}', nickname='{self.nickname}')>"
    
    def to_dict(self):
        """转换为字典，排除敏感信息"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'remark': self.remark,
            'dept_id': self.dept_id,
            'post_ids': self.post_ids,
            'email': self.email,
            'mobile': self.mobile,
            'sex': self.sex,
            'avatar': self.avatar,
            'status': self.status,
            'login_ip': self.login_ip,
            'login_date': self.login_date.isoformat() if self.login_date else None,
            'creator': self.creator,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'updater': self.updater,
            'update_time': self.update_time.isoformat() if self.update_time else None,
            'tenant_id': self.tenant_id
        }
    
    def is_active(self):
        """检查用户是否处于正常状态"""
        return self.status == 0 and not self.deleted
