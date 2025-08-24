from fastapi import APIRouter, HTTPException, Request
from app.services.user_service import UserService
from app.schemas.user_schema import (
    UserLoginRequest, 
    UserRegisterRequest, 
    UserResponse, 
    LoginResponse, 
    RegisterResponse,
    ErrorResponse,
    SuccessResponse
)
from app.models.user import SystemUser

router = APIRouter(prefix="/auth", tags=["认证管理"])



@router.post("/login", response_model=LoginResponse)
async def user_login(
    login_data: UserLoginRequest,
    request: Request
):
    """
    用户登录
    
    Args:
        login_data: 登录数据
        request: 请求对象
        
    Returns:
        登录结果
    """
    try:
        # 验证用户
        user = UserService.authenticate_user(login_data.username, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=401, 
                detail="用户名或密码错误"
            )
        
        # 更新登录信息
        client_ip = request.client.host if request.client else "unknown"
        UserService.update_login_info(user.id, client_ip)
        
        # 构建响应数据
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            mobile=user.mobile,
            avatar=user.avatar,
            status=user.status,
            login_date=user.login_date,
            create_time=user.create_time
        )
        
        return LoginResponse(
            code=200,
            message="登录成功",
            data=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"登录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="登录失败")

@router.post("/register", response_model=RegisterResponse)
async def user_register(
    register_data: UserRegisterRequest
):
    """
    用户注册
    
    Args:
        register_data: 注册数据
        
    Returns:
        注册结果
    """
    try:
        # 创建用户
        new_user = UserService.create_user(register_data)
        
        if not new_user:
            raise HTTPException(status_code=400, detail="用户创建失败，用户名可能已存在")
        
        # 构建响应数据
        user_response = UserResponse(
            id=new_user.id,
            username=new_user.username,
            nickname=new_user.nickname,
            email=new_user.email,
            mobile=new_user.mobile,
            avatar=new_user.avatar,
            status=new_user.status,
            login_date=new_user.login_date,
            create_time=new_user.create_time
        )
        
        return RegisterResponse(
            code=200,
            message="注册成功",
            data=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"注册失败: {str(e)}")
        raise HTTPException(status_code=500, detail="注册失败")

@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: int
):
    """
    获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        用户信息
    """
    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return UserResponse(
            id=user.id,
            username=user.username,
            nickname=user.nickname,
            email=user.email,
            mobile=user.mobile,
            avatar=user.avatar,
            status=user.status,
            login_date=user.login_date,
            create_time=user.create_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取用户信息失败")

@router.post("/create-admin")
async def create_default_admin():
    """
    创建默认管理员账户
    """
    try:
        UserService.create_default_admin()
        return SuccessResponse(
            code=200,
            message="默认管理员账户创建成功",
            data={
                "username": "admin",
                "password": "123456"
            }
        )
    except Exception as e:
        print(f"创建默认管理员失败: {str(e)}")
        raise HTTPException(status_code=500, detail="创建默认管理员失败")
