from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common.response import BaseResp, PageParam

class ModelBase(BaseModel):
    key_id: int = Field(..., description="API 密钥编号")
    name: str = Field(..., description="模型名字")
    model: str = Field(..., description="模型标识")
    platform: str = Field(..., description="模型平台")
    type: int = Field(..., description="模型类型")
    sort: int = Field(..., description="排序")
    status: int = Field(..., description="状态")
    
    # 模型参数
    temperature: Optional[float] = Field(None, description="温度参数")
    max_tokens: Optional[int] = Field(None, description="单条回复的最大 Token 数量")
    max_contexts: Optional[int] = Field(None, description="上下文的最大 Message 数量")

class ModelCreate(ModelBase):
    pass

class ModelUpdate(ModelBase):
    id: int = Field(..., description="编号")

class ModelResp(ModelBase, BaseResp):
    # 额外包含 API 密钥信息
    api_key_name: Optional[str] = Field(None, description="API 密钥名称")
    
    class Config:
        from_attributes = True

class ModelPageReq(PageParam):
    name: Optional[str] = Field(None, description="模型名字")
    platform: Optional[str] = Field(None, description="模型平台")
    type: Optional[int] = Field(None, description="模型类型")
    status: Optional[int] = Field(None, description="状态")
