from langchain_openai import ChatOpenAI
from app.config.setting import settings

def get_chat_openai_model():
    """Initialize and return a ChatOpenAI model using settings."""
    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPERATURE,
        api_key=settings.MODEL_API_KEY,
        base_url=settings.MODEL_BASE_URL
    )
    return model 