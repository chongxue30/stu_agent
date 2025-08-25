from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common.response import BaseResp, PageParam

class ApiKeyBase(BaseModel):
    name: str = Field(..., description="名称")
    api_key: str = Field(..., description="密钥")
    platform: str = Field(..., description="平台")
    url: Optional[str] = Field(None, description="自定义 API 地址")
    status: int = Field(..., description="状态")

class ApiKeyCreate(ApiKeyBase):
    pass

class ApiKeyUpdate(ApiKeyBase):
    id: int = Field(..., description="编号")

class ApiKeyResp(ApiKeyBase, BaseResp):
    pass

class ApiKeyPageReq(PageParam):
    name: Optional[str] = Field(None, description="名称")
    platform: Optional[str] = Field(None, description="平台")
    status: Optional[int] = Field(None, description="状态")
