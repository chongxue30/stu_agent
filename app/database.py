from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.setting import settings
import logging

logger = logging.getLogger(__name__)

def get_mysql_uri():
    return f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?charset=utf8mb4"

# 创建同步引擎
engine = create_engine(
    get_mysql_uri(), 
    echo=True,
    pool_pre_ping=True,  # 连接池预检查
    pool_recycle=3600    # 连接回收时间（秒）
)

# 创建同步会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """创建所有表"""
    try:
        # 导入所有模型以确保它们被注册
        from app.models.user import SystemUser
        
        # 创建表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        return True
    except Exception as e:
        logger.error(f"创建数据库表失败: {str(e)}")
        return False

def drop_tables():
    """删除所有表"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("数据库表删除成功")
        return True
    except Exception as e:
        logger.error(f"删除数据库表失败: {str(e)}")
        return False