from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ai.api_key import ApiKeyService
from app.schemas.ai.api_key import (
    ApiKeyCreate,
    ApiKeyUpdate,
    ApiKeyResp,
    ApiKeyPageReq
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List

router = APIRouter(prefix="/api-key", tags=["API密钥管理"])

@router.post("/create", response_model=ResponseModel[ApiKeyResp])
def create_api_key(
    api_key_in: ApiKeyCreate,
    db: Session = Depends(get_db)
):
    """
    创建 API 密钥
    """
    return ApiKeyService.create_api_key(db=db, api_key_in=api_key_in)

@router.put("/update", response_model=ResponseModel[ApiKeyResp])
def update_api_key(
    api_key_in: ApiKeyUpdate,
    db: Session = Depends(get_db)
):
    """
    更新 API 密钥
    """
    return ApiKeyService.update_api_key(db=db, api_key_in=api_key_in)

@router.delete("/delete/{id}", response_model=ResponseModel[ApiKeyResp])
def delete_api_key(
    id: int,
    db: Session = Depends(get_db)
):
    """
    删除 API 密钥
    """
    return ApiKeyService.delete_api_key(db=db, id=id)

@router.get("/get/{id}", response_model=ResponseModel[ApiKeyResp])
def get_api_key(
    id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个 API 密钥
    """
    return ApiKeyService.get_api_key(db=db, id=id)

@router.get("/simple-list", response_model=ResponseModel[List[ApiKeyResp]])
def get_simple_list(
    status: int = 0,
    db: Session = Depends(get_db)
):
    """
    获取简单 API 密钥列表
    """
    return ApiKeyService.get_api_keys_by_status(db=db, status=status)

@router.get("/page", response_model=ResponseModel[PageResult[ApiKeyResp]])
def get_api_key_page(
    page: ApiKeyPageReq = Depends(),
    db: Session = Depends(get_db)
):
    """
    获取 API 密钥分页列表
    """
    return ApiKeyService.get_api_key_page(db=db, page=page)
