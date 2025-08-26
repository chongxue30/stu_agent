from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common.response import BaseResp, PageParam

class ChatRoleBase(BaseModel):
    user_id: Optional[int] = Field(None, description="用户编号")
    model_id: Optional[int] = Field(None, description="模型编号")
    name: str = Field(..., description="角色名称")
    avatar: str = Field(..., description="头像")
    category: Optional[str] = Field(None, description="角色类别")
    sort: int = Field(0, description="角色排序")
    description: str = Field(..., description="角色描述")
    system_message: Optional[str] = Field(None, description="角色上下文")
    knowledge_ids: Optional[str] = Field(None, description="关联的知识库编号数组")
    tool_ids: Optional[str] = Field(None, description="关联的工具编号数组")
    public_status: bool = Field(..., description="是否公开")
    status: Optional[int] = Field(0, description="状态")

class ChatRoleCreate(ChatRoleBase):
    pass

class ChatRoleUpdate(ChatRoleBase):
    id: int = Field(..., description="角色ID")

class ChatRoleResp(ChatRoleBase, BaseResp):
    model_name: Optional[str] = Field(None, description="模型名称")

class ChatRolePageReq(PageParam):
    name: Optional[str] = Field(None, description="角色名称")
    category: Optional[str] = Field(None, description="角色类别")
    status: Optional[int] = Field(None, description="状态")
    public_status: Optional[bool] = Field(None, description="是否公开")

class ChatRoleSimpleResp(BaseModel):
    id: int = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    avatar: str = Field(..., description="头像")
    category: Optional[str] = Field(None, description="角色类别")
    description: str = Field(..., description="角色描述")
    system_message: Optional[str] = Field(None, description="角色上下文")
    
    class Config:
        from_attributes = True
