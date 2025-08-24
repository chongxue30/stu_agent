from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.user import SystemUser
from app.utils.password import hash_password, verify_password, generate_default_password
from app.schemas.user_schema import UserRegisterRequest
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserService:
    """用户服务类"""
    
    @staticmethod
    def get_db() -> Session:
        """获取数据库会话"""
        return next(get_db())
    
    @staticmethod
    def create_user(user_data: UserRegisterRequest) -> Optional[SystemUser]:
        """创建新用户"""
        try:
            db = UserService.get_db()
            
            # 检查用户名是否已存在
            existing_user = db.query(SystemUser).filter(
                SystemUser.username == user_data.username,
                SystemUser.deleted == False
            ).first()
            
            if existing_user:
                logger.warning(f"用户名 {user_data.username} 已存在")
                return None
            
            # 创建新用户
            hashed_password = hash_password(user_data.password)
            new_user = SystemUser(
                username=user_data.username,
                password=hashed_password,
                nickname=user_data.nickname,
                email=user_data.email or "",
                mobile=user_data.mobile or "",
                remark=user_data.remark or "",
                status=0,  # 默认激活状态
                creator="system",
                tenant_id=0
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"用户 {user_data.username} 创建成功")
            return new_user
            
        except IntegrityError as e:
            logger.error(f"创建用户失败 - 数据库完整性错误: {str(e)}")
            db.rollback()
            return None
        except Exception as e:
            logger.error(f"创建用户失败: {str(e)}")
            db.rollback()
            return None
        finally:
            db.close()
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[SystemUser]:
        """用户认证"""
        try:
            db = UserService.get_db()
            
            # 查找用户
            user = db.query(SystemUser).filter(
                SystemUser.username == username,
                SystemUser.deleted == False
            ).first()
            
            if not user:
                logger.warning(f"用户 {username} 认证失败: 用户不存在")
                return None
            
            # 检查用户状态
            if user.status != 0:
                logger.warning(f"用户 {username} 认证失败: 状态异常 {user.status}")
                return None
            
            # 验证密码
            if not verify_password(password, user.password):
                logger.warning(f"用户 {username} 认证失败: 密码错误")
                return None
            
            logger.info(f"用户 {username} 认证成功")
            return user
            
        except Exception as e:
            logger.error(f"用户认证失败: {str(e)}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def update_login_info(user_id: int, login_ip: str) -> bool:
        """更新用户登录信息"""
        try:
            db = UserService.get_db()
            
            user = db.query(SystemUser).filter(SystemUser.id == user_id).first()
            if not user:
                return False
            
            user.login_ip = login_ip
            user.login_date = datetime.now()
            user.updater = "system"
            user.update_time = datetime.now()
            
            db.commit()
            logger.info(f"用户 {user.username} 登录信息更新成功")
            return True
            
        except Exception as e:
            logger.error(f"更新登录信息失败: {str(e)}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[SystemUser]:
        """根据ID获取用户"""
        try:
            db = UserService.get_db()
            user = db.query(SystemUser).filter(
                SystemUser.id == user_id,
                SystemUser.deleted == False
            ).first()
            return user
        except Exception as e:
            logger.error(f"获取用户失败: {str(e)}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[SystemUser]:
        """根据用户名获取用户"""
        try:
            db = UserService.get_db()
            user = db.query(SystemUser).filter(
                SystemUser.username == username,
                SystemUser.deleted == False
            ).first()
            
            if not user:
                return None
            
            return user
        except Exception as e:
            logger.error(f"获取用户失败: {str(e)}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def create_default_admin() -> Optional[SystemUser]:
        """创建默认管理员用户"""
        try:
            db = UserService.get_db()
            
            # 检查是否已存在管理员
            admin = db.query(SystemUser).filter(
                SystemUser.username == "admin",
                SystemUser.deleted == False
            ).first()
            
            if admin:
                logger.info("默认管理员用户已存在")
                return admin
            
            # 创建管理员用户
            admin_user = SystemUser(
                username="admin",
                password=hash_password("admin123"),
                nickname="系统管理员",
                remark="系统默认管理员账户",
                status=0,
                creator="system",
                tenant_id=0
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            logger.info(f"默认管理员用户创建成功，用户名: admin，密码: admin123")
            return admin_user
            
        except Exception as e:
            logger.error(f"创建默认管理员失败: {str(e)}")
            db.rollback()
            return None
        finally:
            db.close() 