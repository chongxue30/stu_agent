from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user_id
from app.services.ai.chat_conversation import ChatConversationService
from app.schemas.ai.chat_conversation import (
    ChatConversationCreate, ChatConversationUpdate, ChatConversationPageReq, ChatConversationResp, ChatConversationSimpleResp
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List

router = APIRouter(prefix="/chat-conversation", tags=["AI聊天对话管理"])

@router.post("/create", response_model=ResponseModel[int])
def create_conversation(
    conversation_in: ChatConversationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """创建聊天对话"""
    return ChatConversationService.create_conversation(db=db, conversation_in=conversation_in, user_id=user_id)

@router.put("/update", response_model=ResponseModel[bool])
def update_conversation(
    conversation_in: ChatConversationUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """更新聊天对话"""
    return ChatConversationService.update_conversation(db=db, conversation_in=conversation_in, user_id=user_id)

@router.delete("/delete/{id}", response_model=ResponseModel[bool])
def delete_conversation(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除聊天对话"""
    return ChatConversationService.delete_conversation(db=db, id=id, user_id=user_id)

@router.get("/get/{id}", response_model=ResponseModel[ChatConversationResp])
def get_conversation(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取单个对话"""
    return ChatConversationService.get_conversation(db=db, id=id, user_id=user_id)

@router.get("/list", response_model=ResponseModel[List[ChatConversationSimpleResp]], summary="获得我的聊天对话列表")
def get_my_chat_conversation_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获得当前登录用户的聊天对话列表"""
    return ChatConversationService.get_conversation_list(db=db, user_id=user_id)

@router.post("/toggle-pin/{id}", response_model=ResponseModel[bool])
def toggle_conversation_pin(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """切换对话置顶状态"""
    return ChatConversationService.toggle_pin(db=db, id=id, user_id=user_id)

@router.get("/page", response_model=ResponseModel[PageResult[ChatConversationResp]])
def get_conversation_page(
    page: ChatConversationPageReq = Depends(),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """分页获取对话列表"""
    return ChatConversationService.get_conversation_page(db=db, page=page, user_id=user_id)
