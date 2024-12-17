from zhipuai import ZhipuAI
from app.config.setting import settings
from app.aiengine.model import get_chat_openai_model  # 更新导入路径
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from fastapi import APIRouter, HTTPException

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key=settings.MODEL_API_KEY)

# 使用 app.aiengine.model 中的函数创建模型
model = get_chat_openai_model()

# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个乐于助人的助手。用{language}尽你所能回答所有问题。'),
    MessagesPlaceholder(variable_name='my_msg')
])

# 得到链
chain = prompt_template | model

# 保存聊天的历史记录
store = {}  # 所有用户的聊天记录都保存到store。key: sessionId,value: 历史聊天记录对象

# 获取会话历史记录
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 定义消息处理
do_message = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='my_msg'  # 每次聊天时候发送msg的key
)

def chat_with_model(message: str, session_id: str, language: str = '中文'):
    config = {'configurable': {'session_id': session_id}}
    try:
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
        print("Error during chat:", str(e))
        return "处理消息时发生错误。"

# 示例调用
if __name__ == "__main__":
    # 第一轮
    resp1 = chat_with_model('你好啊！ 我是LaoXiao', 'zs1234')
    print(resp1)

    # 第二轮
    resp2 = chat_with_model('请问：我的名字是什么？', 'zs1234')
    print(resp2)

    # 第三轮：流式输出
    for resp in do_message.stream({'my_msg': [HumanMessage(content='请给我讲一个笑话？')], 'language': 'English'},
                                  config={'configurable': {'session_id': 'zs1234'}}):
        print(resp.content, end='')
