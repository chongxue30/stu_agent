from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.common.response import BaseResp, PageParam

class ChatMessageBase(BaseModel):
    conversation_id: int = Field(..., description="对话编号")
    reply_id: Optional[int] = Field(None, description="回复编号")
    user_id: int = Field(..., description="用户编号")
    role_id: Optional[int] = Field(None, description="角色编号")
    type: str = Field(..., description="消息类型")
    model: str = Field(..., description="模型标识")
    model_id: int = Field(..., description="模型编号")
    content: str = Field(..., description="消息内容")
    use_context: bool = Field(True, description="是否携带上下文")
    segment_ids: Optional[str] = Field(None, description="段落编号数组")

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(ChatMessageBase):
    id: int = Field(..., description="消息ID")

class ChatMessageResp(ChatMessageBase, BaseResp):
    user_id: Optional[int] = Field(None, description="用户编号")
    
    class Config:
        from_attributes = True

class ChatMessagePageReq(PageParam):
    conversation_id: Optional[int] = Field(None, description="对话编号")
    type: Optional[str] = Field(None, description="消息类型")
    user_id: Optional[int] = Field(None, description="用户编号")

class ChatMessageSendReq(BaseModel):
    conversation_id: int = Field(..., description="对话编号")
    content: str = Field(..., description="消息内容")
    role_id: Optional[int] = Field(None, description="角色编号")
    use_context: bool = Field(True, description="是否携带上下文")

class ChatMessageSendResp(BaseModel):
    message_id: int = Field(..., description="消息ID")
    content: str = Field(..., description="AI回复内容")
    conversation_id: int = Field(..., description="对话编号")
    model: str = Field(..., description="使用的模型")
    
    class Config:
        from_attributes = True

class ChatMessageSimpleResp(BaseModel):
    id: int = Field(..., description="消息ID")
    type: str = Field(..., description="消息类型")
    content: str = Field(..., description="消息内容")
    create_time: Optional[str] = Field(None, description="创建时间")
    
    class Config:
        from_attributes = True
