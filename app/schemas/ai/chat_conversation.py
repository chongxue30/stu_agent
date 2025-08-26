from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common.response import BaseResp, PageParam

class ChatConversationBase(BaseModel):
    role_id: Optional[int] = Field(None, description="聊天角色ID")
    title: str = Field(..., description="对话标题")
    model_id: int = Field(..., description="模型编号")
    model: str = Field(..., description="模型标识")
    pinned: bool = Field(False, description="是否置顶")
    system_message: Optional[str] = Field(None, description="角色设定")
    temperature: float = Field(..., description="温度参数")
    max_tokens: int = Field(..., description="单条回复的最大 Token 数量")
    max_contexts: int = Field(..., description="上下文的最大 Message 数量")

class ChatConversationCreate(ChatConversationBase):
    pass

class ChatConversationUpdate(ChatConversationBase):
    id: int = Field(..., description="对话ID")

class ChatConversationResp(ChatConversationBase, BaseResp):
    user_id: Optional[int] = Field(None, description="用户编号")
    pinned_time: Optional[str] = Field(None, description="置顶时间")
    
    class Config:
        from_attributes = True

class ChatConversationPageReq(PageParam):
    title: Optional[str] = Field(None, description="对话标题")
    model_id: Optional[int] = Field(None, description="模型编号")
    role_id: Optional[int] = Field(None, description="角色ID")
    pinned: Optional[bool] = Field(None, description="是否置顶")

class ChatConversationSimpleResp(BaseModel):
    id: int = Field(..., description="对话ID")
    title: str = Field(..., description="对话标题")
    model: str = Field(..., description="模型标识")
    pinned: bool = Field(..., description="是否置顶")
    create_time: Optional[str] = Field(None, description="创建时间")
    
    class Config:
        from_attributes = True
