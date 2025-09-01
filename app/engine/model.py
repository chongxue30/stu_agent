from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_chat_openai_model(api_key: str = None):
    """Initialize and return a ChatOpenAI model using settings."""
    if api_key is None:
        api_key = settings.MODEL_API_KEY
        
    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPERATURE,
        api_key=api_key,
        base_url=settings.MODEL_BASE_URL
    )
    return model 