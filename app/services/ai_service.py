from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User  # Assuming you have a User model
from app.services.generate.ai_model import generate_sql_query
from app.services.chat.chat import chat_with_model  # Import the chat function
from fastapi import HTTPException

def process_request():
    # Create a new database session
    session = SessionLocal()
    try:
        # Example query: Get all users
        users = session.query(User).all()
        # Process the query results
        user_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
        return user_data
    except Exception as e:
        # Handle exceptions
        return f"An error occurred: {str(e)}"
    finally:
        # Close the session
        session.close()

def ai_support(question: str):
    try:
        result = ai_support_service(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def ai_support_service(question: str):
    # Example usage of the imported function
    sql_query = generate_sql_query(question)
    print("Generated SQL Query in ai_service:", sql_query)
    return sql_query

def chat_service(message: str, session_id: str):
    try:
        # Ensure the message is of the correct type
        if not isinstance(message, str):
            raise ValueError("Input message must be a string.")
        
        # Use the chat_with_model function
        response = chat_with_model(message, session_id)
        print("Chat response in ai_service:", response)
        return response
    except ValueError as ve:
        # Handle specific value errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Handle general exceptions
        print("Error during chat:", str(e))
        return "An error occurred while processing your message."
