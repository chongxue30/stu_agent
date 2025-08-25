from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class TokenPayload(BaseModel):
    """Token 载荷"""
    sub: Optional[int] = None
    exp: Optional[datetime] = None

class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str

class UserLoginRequest(BaseModel):
    """用户登录请求"""
    username: str = Field(..., min_length=1, max_length=30, description="用户名")
    password: str = Field(..., min_length=1, max_length=100, description="密码")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError('用户名不能为空')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v.strip():
            raise ValueError('密码不能为空')
        return v.strip()

class UserRegisterRequest(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=1, max_length=30, description="用户名")
    password: str = Field(..., min_length=6, max_length=20, description="密码")
    nickname: str = Field(..., min_length=1, max_length=30, description="昵称")
    email: Optional[str] = Field(None, max_length=50, description="邮箱")
    mobile: Optional[str] = Field(None, max_length=11, description="手机号")
    remark: Optional[str] = Field(None, max_length=500, description="备注")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError('用户名不能为空')
        if len(v.strip()) < 3:
            raise ValueError('用户名至少3位')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v.strip():
            raise ValueError('密码不能为空')
        if len(v.strip()) < 6:
            raise ValueError('密码至少6位')
        return v.strip()
    
    @validator('nickname')
    def validate_nickname(cls, v):
        if not v.strip():
            raise ValueError('昵称不能为空')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        if v and v.strip():
            # 简单的邮箱格式验证
            if '@' not in v or '.' not in v:
                raise ValueError('邮箱格式不正确')
            return v.strip()
        return v

class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    nickname: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    avatar: Optional[str] = None
    status: int
    login_date: Optional[datetime] = None
    create_time: datetime
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    """登录响应"""
    code: int = 200
    message: str = "登录成功"
    data: UserResponse
    access_token: str
    token_type: str = "bearer"

class RegisterResponse(BaseModel):
    """注册响应"""
    code: int = 200
    message: str = "注册成功"
    data: UserResponse

class ErrorResponse(BaseModel):
    """错误响应"""
    code: int
    message: str
    data: Optional[dict] = None

class SuccessResponse(BaseModel):
    """成功响应"""
    code: int = 200
    message: str = "操作成功"
    data: Optional[dict] = None