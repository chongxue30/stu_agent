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
    DATABASE_NAME: str = "rouyi-vue-pro"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "chongxue=10293X"

    # JWT
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # AI Model settings
    MODEL_NAME: str = "glm-4-0520"
    MODEL_TEMPERATURE: float = 0.0
    MODEL_API_KEY: str = ""
    MODEL_BASE_URL: str = "https://open.bigmodel.cn/api/paas/v4/"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
