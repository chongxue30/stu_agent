from app.database import create_tables
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

def init_database():
    """初始化数据库"""
    try:
        # 创建表
        if create_tables():
            logger.info("数据库表创建成功")
            
            # 创建默认管理员用户
            admin_user = UserService.create_default_admin()
            if admin_user:
                logger.info("默认管理员用户创建成功")
            else:
                logger.warning("默认管理员用户创建失败或已存在")
                
            return True
        else:
            logger.error("数据库表创建失败")
            return False
            
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False

def create_test_user():
    """创建测试用户"""
    try:
        from app.schemas.user_schema import UserRegisterRequest
        
        # 创建测试用户
        test_user_data = UserRegisterRequest(
            username="testuser",
            password="test123",
            nickname="测试用户",
            email="test@example.com",
            remark="测试账户"
            )
        
        test_user = UserService.create_user(test_user_data)
        if test_user:
            logger.info("测试用户创建成功")
            return True
        else:
            logger.warning("测试用户创建失败")
            return False
            
    except Exception as e:
        logger.error(f"创建测试用户失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 初始化数据库
    if init_database():
        print("✅ 数据库初始化成功")
        
        # 创建测试用户
        if create_test_user():
            print("✅ 测试用户创建成功")
        else:
            print("⚠️ 测试用户创建失败")
    else:
        print("❌ 数据库初始化失败")
