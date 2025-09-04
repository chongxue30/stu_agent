from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from app.models.ai.model import Model
from app.models.ai.api_key import ApiKey
from app.crud.ai.model import model as model_crud
from app.crud.ai.api_key import api_key as api_key_crud
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ModelFactory:
    """AI模型工厂类，用于创建和管理AI模型实例"""
    
    PLATFORM_CONFIGS = {
        "deepseek": {
            "model_class": ChatOpenAI,
            "default_url": "https://api.deepseek.com/v1",
            "default_model": "deepseek-chat"
        },
        "zhipu": {
            "model_class": ChatOpenAI,
            "default_url": "https://open.bigmodel.cn/api/paas/v4",
            "default_model": "glm-4"
        },
        "tongyi": {
            "model_class": ChatOpenAI,
            "default_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "default_model": "qwen-plus"
        },
        "TongYi": {
            "model_class": ChatOpenAI,
            "default_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "default_model": "qwen-plus"
        },
        "openai": {
            "model_class": ChatOpenAI,
            "default_url": "https://api.openai.com/v1",
            "default_model": "gpt-3.5-turbo"
        }
    }

    @classmethod
    def get_or_create_chat_model(cls, platform: str, api_key: str, url: str = None, model_name: str = None) -> ChatOpenAI:
        """
        根据平台创建或获取聊天模型实例（参考芋道项目模式）
        
        Args:
            platform: 平台名称 (支持任意平台，优先使用数据库配置)
            api_key: API密钥
            url: API地址（可选，使用默认值）
            model_name: 模型名称（可选，使用默认值）
            
        Returns:
            ChatOpenAI: 模型实例
        """
        platform_lower = platform.lower()
        platform_config = cls.PLATFORM_CONFIGS.get(platform_lower)
        
        # 优先使用传入的参数，其次使用配置中的默认值
        if platform_config:
            base_url = url or platform_config["default_url"]
            model = model_name or platform_config["default_model"]
        else:
            # 如果平台不在配置中，使用传入的参数
            base_url = url
            model = model_name
            
            # 如果都没有提供，给出友好的错误提示
            if not base_url or not model:
                raise ValueError(f"平台 {platform} 未在配置中定义，请确保数据库中的API密钥和模型配置完整")
        
        logger.info(f"创建 {platform} 模型实例: model={model}, base_url={base_url}")
        
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=0.7,
            max_tokens=2000,
            timeout=15,
        )

    @classmethod
    def create_model_by_id(cls, db: Session, model_id: int, user_id: int) -> ChatOpenAI:
        """
        根据模型ID创建AI模型实例（参考芋道项目的 AiModelServiceImpl.getChatModel）
        
        Args:
            db: 数据库会话
            model_id: 模型ID
            user_id: 用户ID
            
        Returns:
            ChatOpenAI: 模型实例
        """
        # 1. 获取模型配置
        model_config = (
            db.query(Model)
            .filter(
                Model.id == model_id,
                Model.status == 1,
                Model.deleted.is_(False),
            )
            .first()
        )
        if not model_config:
            raise ValueError(f"Model {model_id} not found or inactive/deleted")

        logger.info(f"找到模型配置: {model_config.name} (ID: {model_id})")

        # 2. 获取API密钥配置
        api_key_config = (
            db.query(ApiKey)
            .filter(
                ApiKey.id == model_config.key_id,
                ApiKey.status == 1,
                ApiKey.deleted.is_(False),
            )
            .first()
        )
        if not api_key_config:
            raise ValueError(f"API key {model_config.key_id} not found or inactive/deleted")

        logger.info(f"找到API密钥配置: {api_key_config.name} (ID: {model_config.key_id})")

        # 3. 创建模型实例
        return cls.get_or_create_chat_model(
            platform=model_config.platform,
            api_key=api_key_config.api_key,
            url=api_key_config.url,
            model_name=model_config.model
        )

    @classmethod
    def create_model_with_config(cls, 
                               db: Session, 
                               model_id: int, 
                               user_id: int, 
                               custom_config: Dict[str, Any] = None) -> ChatOpenAI:
        """
        使用自定义配置创建AI模型实例
        
        Args:
            db: 数据库会话
            model_id: 模型ID
            user_id: 用户ID
            custom_config: 自定义配置参数
            
        Returns:
            ChatOpenAI: 模型实例
        """
        # 创建基础模型
        model = cls.create_model_by_id(db, model_id, user_id)
        
        # 如果有自定义配置，重新创建模型实例
        if custom_config:
            # 获取当前模型的配置
            current_config = {
                "model": model.model_name,
                "api_key": model.openai_api_key,
                "base_url": model.openai_api_base,
                "temperature": getattr(model, 'temperature', 0.7),
                "max_tokens": getattr(model, 'max_tokens', 2000),
                "timeout": 15,
            }
            # 应用自定义配置
            current_config.update(custom_config)
            
            # 重新创建模型实例
            model = ChatOpenAI(**current_config)
        
        return model

def get_chat_openai_model(api_key: str = None):
    """
    获取智谱AI模型实例（兼容旧代码）
    
    Args:
        api_key: API密钥，如果不提供则使用配置文件中的默认值
        
    Returns:
        ChatOpenAI: 模型实例
    """
    if api_key is None:
        api_key = settings.MODEL_API_KEY
        
    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPERATURE,
        api_key=api_key,
        base_url=settings.MODEL_BASE_URL,
        max_tokens=4096,  # 默认值
        timeout=60,
    )
    return model

def test_model(db: Session, model_id: int, user_id: int) -> bool:
    """
    测试模型是否可用
    
    Args:
        db: 数据库会话
        model_id: 模型ID
        user_id: 用户ID
        
    Returns:
        bool: 测试是否成功
    """
    try:
        model = ModelFactory.create_model_by_id(db, model_id, user_id)
        response = model.invoke("你好，请简单介绍一下你自己")
        print(f"模型 {model_id} 测试成功!")
        print("响应:", response.content)
        return True
    except Exception as e:
        print(f"模型 {model_id} 测试失败: {str(e)}")
        return False