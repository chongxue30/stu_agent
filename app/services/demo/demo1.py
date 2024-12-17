from zhipuai import ZhipuAI
import os
# 使用GLM自己的

# api_key = os.getenv('API_KEY')
# print(api_key)
client = ZhipuAI(api_key='c21bc97ad4ebb3b869dbbcf485c2d496.46T24YwnW8zSgUzq')

response = client.chat.completions.create(
    model='glm-4-0520',
    messages=[
        {'role': "user", 'content': '请介绍一下denstu？'}
    ],
    stream=True
)

# 流式输出的正确处理方式
for s in response:
    # 每个流式响应片段可能包含部分内容
    print(s.choices[0].delta.content, end='')

# 如果需要完整的响应内容，可以将其拼接起来
full_content = ''
for s in response:
    full_content += s.choices[0].delta.content

print("\n完整的响应内容:")
print(full_content)