import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "rm-bp18ni4370md7m57dzo.mysql.rds.aliyuncs.com")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", 3306)
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "test_db8")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "chongxue=10293X")

    # Model settings - 智谱 AI
    MODEL_NAME: str = os.getenv("MODEL_NAME", "glm-4-0520")
    MODEL_TEMPERATURE: float = os.getenv("MODEL_TEMPERATURE", 0.0)
    MODEL_API_KEY: str = os.getenv("MODEL_API_KEY", "c21bc97ad4ebb3b869dbbcf485c2d496.46T24YwnW8zSgUzq")
    MODEL_BASE_URL: str = os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")

    # DeepSeek Model settings
    DEEPSEEK_MODEL_NAME: str = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "sk-2834347b29be42299f548adee940b65d")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_TEMPERATURE: float = os.getenv("DEEPSEEK_TEMPERATURE", 0.7)
    DEEPSEEK_MAX_TOKENS: int = os.getenv("DEEPSEEK_MAX_TOKENS", 4096)

    # Other settings
    DEBUG: bool = os.getenv("DEBUG", True)

    class Config:
        env_file = ".env"

# Create a settings instance
settings = Settings()
