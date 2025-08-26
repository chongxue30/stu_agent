from zhipuai import ZhipuAI
from app.core.config import settings
from app.engine.model import get_chat_openai_model  # 智谱 AI 模型
from app.engine.deepseek_model import get_deepseek_model  # DeepSeek 模型
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from fastapi import APIRouter, HTTPException

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key=settings.MODEL_API_KEY)

# 使用 app.aiengine.model 中的函数创建模型
zhipu_model = get_chat_openai_model()
deepseek_model = get_deepseek_model()

# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个乐于助人的助手。用{language}尽你所能回答所有问题。'),
    MessagesPlaceholder(variable_name='my_msg')
])

# 得到链 - 智谱 AI
zhipu_chain = prompt_template | zhipu_model

# 得到链 - DeepSeek
deepseek_chain = prompt_template | deepseek_model

# 保存聊天的历史记录
store = {}  # 所有用户的聊天记录都保存到store。key: sessionId,value: 历史聊天记录对象

# 获取会话历史记录
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 定义消息处理 - 智谱 AI
do_message_zhipu = RunnableWithMessageHistory(
    zhipu_chain,
    get_session_history,
    input_messages_key='my_msg'  # 每次聊天时候发送msg的key
)

# 定义消息处理 - DeepSeek
do_message_deepseek = RunnableWithMessageHistory(
    deepseek_chain,
    get_session_history,
    input_messages_key='my_msg'  # 每次聊天时候发送msg的key
)

def chat_with_model(message: str, session_id: str, language: str = '中文', model_type: str = 'deepseek'):
    """
    聊天函数，支持选择不同的模型
    
    Args:
        message: 用户消息
        session_id: 会话ID
        language: 语言
        model_type: 模型类型 ('deepseek' 或 'zhipu')
    """
    config = {'configurable': {'session_id': session_id}}
    
    try:
        # 根据模型类型选择对应的处理链
        if model_type.lower() == 'deepseek':
            do_message = do_message_deepseek
            print(f"使用 DeepSeek 模型处理消息: {message}")
        else:
            do_message = do_message_zhipu
            print(f"使用智谱 AI 模型处理消息: {message}")
        
        # 处理消息
        response = do_message.invoke(
            {
                'my_msg': [HumanMessage(content=message)],
                'language': language
            },
            config=config
        )
        return response.content
    except Exception as e:
        print(f"Error during chat with {model_type}: {str(e)}")
        return f"处理消息时发生错误: {str(e)}"

def chat_with_deepseek(message: str, session_id: str, language: str = '中文'):
    """专门使用 DeepSeek 模型的聊天函数"""
    return chat_with_model(message, session_id, language, 'deepseek')

def chat_with_zhipu(message: str, session_id: str, language: str = '中文'):
    """专门使用智谱 AI 模型的聊天函数"""
    return chat_with_model(message, session_id, language, 'zhipu')

# 示例调用
if __name__ == "__main__":
    # 测试 DeepSeek 模型
    print("=== 测试 DeepSeek 模型 ===")
    resp1 = chat_with_deepseek('你好啊！ 我是LaoXiao', 'ds1234')
    print(resp1)

    # 测试智谱 AI 模型
    print("\n=== 测试智谱 AI 模型 ===")
    resp2 = chat_with_zhipu('你好啊！ 我是LaoXiao', 'zp1234')
    print(resp2)
