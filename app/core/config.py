from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base
    PROJECT_NAME: str = "AI Support API"
    PROJECT_DESCRIPTION: str = "AI 支持服务 API，包含用户认证和AI聊天功能"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Database settings
    DATABASE_HOST: str = "rm-bp18ni4370md7m57dzo.mysql.rds.aliyuncs.com"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "stu_agent"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "chongxue=10293X"

    # JWT
    SECRET_KEY: str = "your-secret-key"  # 请在生产环境中修改
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # AI Model Settings
    # DeepSeek 模型配置
    DEEPSEEK_MODEL_NAME: str = "deepseek-chat"
    DEEPSEEK_TEMPERATURE: float = 0.7
    DEEPSEEK_API_KEY: str = "your-deepseek-api-key"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MAX_TOKENS: int = 4096
    
    # 智谱 AI 模型配置
    MODEL_NAME: str = "glm-4"
    MODEL_TEMPERATURE: float = 0.7
    MODEL_API_KEY: str = "your-zhipu-api-key"
    MODEL_BASE_URL: str = "https://open.bigmodel.cn/api/paas/v4"

    class Config:
        env_file = ".env"
        case_sensitive = True
        # 禁用受保护命名空间检查，避免 model_ 字段的警告
        protected_namespaces = ()

settings = Settings()