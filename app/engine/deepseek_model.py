from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_deepseek_model(api_key: str = None):
    """Initialize and return a DeepSeek model using OpenAI-compatible API."""
    if api_key is None:
        api_key = settings.DEEPSEEK_API_KEY
        
    model = ChatOpenAI(
        model=settings.DEEPSEEK_MODEL_NAME,
        temperature=settings.DEEPSEEK_TEMPERATURE,
        api_key=api_key,
        base_url=settings.DEEPSEEK_BASE_URL,
        max_tokens=settings.DEEPSEEK_MAX_TOKENS,
        timeout=60,
    )
    return model

def get_deepseek_model_with_config(temperature=None, max_tokens=None, api_key: str = None):
    """Initialize and return a DeepSeek model with custom configuration."""
    if api_key is None:
        api_key = settings.DEEPSEEK_API_KEY
        
    # 使用传入的参数，如果没有则使用配置文件中的默认值
    temp = temperature if temperature is not None else settings.DEEPSEEK_TEMPERATURE
    tokens = max_tokens if max_tokens is not None else settings.DEEPSEEK_MAX_TOKENS
    
    model = ChatOpenAI(
        model=settings.DEEPSEEK_MODEL_NAME,
        temperature=temp,
        api_key=api_key,
        base_url=settings.DEEPSEEK_BASE_URL,
        max_tokens=tokens,
        timeout=60,
    )
    return model

# 测试函数
def test_deepseek_model():
    """Test the DeepSeek model with a simple prompt."""
    try:
        model = get_deepseek_model()
        response = model.invoke("你好，请简单介绍一下你自己")
        print("DeepSeek 模型测试成功!")
        print("响应:", response.content)
        return True
    except Exception as e:
        print(f"DeepSeek 模型测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_deepseek_model()
