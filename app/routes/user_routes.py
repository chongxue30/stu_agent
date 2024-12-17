from fastapi import APIRouter
from schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return "hello"
