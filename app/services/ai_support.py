# Import the function from ai_model.py
from app.services.generate.ai_model import generate_sql_query

# Example usage of the imported function
def example_usage():
    question = '请问：一共有多少个员工？'
    sql_query = generate_sql_query(question)
    print("Generated SQL Query in ai_support:", sql_query)

# Call the example usage function
if __name__ == "__main__":
    example_usage() 