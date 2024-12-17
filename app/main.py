from fastapi import FastAPI
from app.routes.ai_support import router as ai_router
from app.database import engine, Base

app = FastAPI()

# Include routers
app.include_router(ai_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)