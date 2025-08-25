from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ai.chat_role import ChatRoleService
from app.schemas.ai.chat_role import (
    ChatRoleCreate,
    ChatRoleUpdate,
    ChatRoleResp,
    ChatRolePageReq
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List

router = APIRouter(prefix="/chat-role", tags=["AI聊天角色管理"])

@router.post("/create", response_model=ResponseModel[ChatRoleResp])
def create_chat_role(
    role_in: ChatRoleCreate,
    db: Session = Depends(get_db)
):
    """
    创建聊天角色
    """
    return ChatRoleService.create_chat_role(db=db, role_in=role_in)

@router.put("/update", response_model=ResponseModel[ChatRoleResp])
def update_chat_role(
    role_in: ChatRoleUpdate,
    db: Session = Depends(get_db)
):
    """
    更新聊天角色
    """
    return ChatRoleService.update_chat_role(db=db, role_in=role_in)

@router.delete("/delete/{id}", response_model=ResponseModel[ChatRoleResp])
def delete_chat_role(
    id: int,
    db: Session = Depends(get_db)
):
    """
    删除聊天角色
    """
    return ChatRoleService.delete_chat_role(db=db, id=id)

@router.get("/get/{id}", response_model=ResponseModel[ChatRoleResp])
def get_chat_role(
    id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个聊天角色
    """
    return ChatRoleService.get_chat_role(db=db, id=id)

@router.get("/category-list", response_model=ResponseModel[List[str]])
def get_category_list(
    db: Session = Depends(get_db)
):
    """
    获取角色分类列表
    """
    return ChatRoleService.get_categories(db=db)

@router.get("/page", response_model=ResponseModel[PageResult[ChatRoleResp]])
def get_chat_role_page(
    page: ChatRolePageReq = Depends(),
    db: Session = Depends(get_db)
):
    """
    获取聊天角色分页列表
    """
    return ChatRoleService.get_chat_role_page(db=db, page=page)
