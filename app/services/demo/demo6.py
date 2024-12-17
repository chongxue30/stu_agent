from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine

# sqlalchemy 初始化MySQL数据库的连接
HOSTNAME = 'rm-bp18ni4370md7m57dzo.mysql.rds.aliyuncs.com'
PORT = '3306'
DATABASE = 'test_db8'
USERNAME = 'root'
PASSWORD = 'chongxue=10293X'
# mysqlclient驱动URL
# MYSQL_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# 使用 PyMySQL 驱动的 URL
MYSQL_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# 创建模型
model = ChatOpenAI(
    model='glm-4-0520',
    temperature=0,
    api_key='c21bc97ad4ebb3b869dbbcf485c2d496.46T24YwnW8zSgUzq',
    base_url='https://open.bigmodel.cn/api/paas/v4/'
)

db = SQLDatabase.from_uri(MYSQL_URI)
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run('select * from t_emp;'))


chian = create_sql_query_chain(llm=model, db=db)
# chian.get_prompts()[0].pretty_print()
resp = chian.invoke({'question': '请问：一共有多少个员工？'})
print('大语言模型生成的SQL：' + resp)
# 提取有效的 SQL 查询
def extract_sql_query(output):
    try:
        # 假设生成的输出格式为 "SQLQuery: ...; SQLResult: ..."
        sql_query = output.split("SQLQuery: ")[1].split(";\n")[0] + ";"
        return sql_query
    except IndexError:
        raise ValueError("无法提取 SQL 查询，请检查输入格式。")

# 使用提取函数
try:
    sql = extract_sql_query(resp)
    print('提取之后的SQL：' + sql)

    # 执行 SQL 查询并打印结果
    result = db.run(sql)
    print("查询结果:", result)
except Exception as e:
    print("执行查询时发生错误:", str(e))
