from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from app.database import get_mysql_uri
from app.aiengine.model import get_chat_openai_model  # Import the function

# Use the function to get the database connection URI
MYSQL_URI = get_mysql_uri()

# Get the ChatOpenAI model
model = get_chat_openai_model()

# Initialize the database
db = SQLDatabase.from_uri(MYSQL_URI)

# Create the SQL query chain
chain = create_sql_query_chain(llm=model, db=db)

def generate_sql_query(question: str) -> str:
    # Invoke the chain with a question
    resp = chain.invoke({'question': question})
    print('大语言模型生成的SQL：' + resp)

    def extract_sql_query(output):
        try:
            sql_query = output.split("SQLQuery: ")[1].split(";\n")[0] + ";"
            return sql_query
        except IndexError:
            raise ValueError("无法提取 SQL 查询，请检查输入格式")

    try:
        sql = extract_sql_query(resp)
        print('提取之后的SQL：' + sql)
        return sql
    except Exception as e:
        print("执行查询时发生错误:", str(e))
        return ""