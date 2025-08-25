from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import json
from app.schemas.common.response import BaseResp, PageParam

class ChatRoleBase(BaseModel):
    user_id: Optional[int] = Field(None, description="用户编号")
    model_id: Optional[int] = Field(None, description="模型编号")
    name: str = Field(..., description="角色名称")
    avatar: str = Field(..., description="头像")
    category: Optional[str] = Field(None, description="角色类别")
    sort: int = Field(default=0, description="角色排序")
    description: str = Field(..., description="角色描述")
    system_message: Optional[str] = Field(None, description="角色上下文")
    knowledge_ids: Optional[List[int]] = Field(None, description="关联的知识库编号数组")
    tool_ids: Optional[List[int]] = Field(None, description="关联的工具编号数组")
    public_status: bool = Field(..., description="是否公开")
    status: Optional[int] = Field(None, description="状态")

    @field_validator("knowledge_ids", "tool_ids", mode="before")
    def validate_json_arrays(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return []
        return v or []

class ChatRoleCreate(ChatRoleBase):
    pass

class ChatRoleUpdate(ChatRoleBase):
    id: int = Field(..., description="编号")

class ChatRoleResp(ChatRoleBase, BaseResp):
    # 额外包含模型信息
    model_name: Optional[str] = Field(None, description="模型名称")
    
    class Config:
        from_attributes = True

class ChatRolePageReq(PageParam):
    name: Optional[str] = Field(None, description="角色名称")
    category: Optional[str] = Field(None, description="角色类别")
    public_status: Optional[bool] = Field(None, description="是否公开")
    status: Optional[int] = Field(None, description="状态")
    user_id: Optional[int] = Field(None, description="用户编号")
