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
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "stu_agent"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = ""

    # JWT
    SECRET_KEY: str = "your-secret-key"  # 请在生产环境中修改
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()