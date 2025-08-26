from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.ai.api_key import api_key
from app.schemas.ai.api_key import ApiKeyCreate, ApiKeyUpdate, ApiKeyPageReq, ApiKeyResp
from app.schemas.common.response import PageResult, ResponseModel
from app.models.ai.api_key import ApiKey

class ApiKeyService:
    @staticmethod
    def create_api_key(db: Session, api_key_in: ApiKeyCreate) -> ResponseModel[ApiKeyResp]:
        # 检查名称是否已存在
        db_api_key = api_key.get_by_name(db, name=api_key_in.name)
        if db_api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="API Key name already exists"
            )
        db_obj = api_key.create(db, obj_in=api_key_in)
        return ResponseModel(data=ApiKeyResp.model_validate(db_obj))

    @staticmethod
    def update_api_key(db: Session, api_key_in: ApiKeyUpdate) -> ResponseModel[ApiKeyResp]:
        # 检查是否存在
        db_api_key = api_key.get(db, id=api_key_in.id)
        if not db_api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found"
            )
        # 检查名称是否已存在（排除自己）
        name_exists = api_key.get_by_name(db, name=api_key_in.name)
        if name_exists and name_exists.id != api_key_in.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="API Key name already exists"
            )
        db_obj = api_key.update(db, db_obj=db_api_key, obj_in=api_key_in)
        return ResponseModel(data=ApiKeyResp.model_validate(db_obj))

    @staticmethod
    def delete_api_key(db: Session, id: int) -> ResponseModel[ApiKeyResp]:
        db_api_key = api_key.get(db, id=id)
        if not db_api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found"
            )
        db_obj = api_key.soft_delete(db, id=id)
        return ResponseModel(data=ApiKeyResp.model_validate(db_obj))
    
    @staticmethod
    def restore_api_key(db: Session, id: int) -> ResponseModel[ApiKeyResp]:
        """恢复已删除的 API 密钥"""
        db_api_key = api_key.get(db, id=id)
        if not db_api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found"
            )
        # 恢复已删除的记录
        db_obj = api_key.restore(db, id=id)
        return ResponseModel(data=ApiKeyResp.model_validate(db_obj))

    @staticmethod
    def get_api_key(db: Session, id: int) -> ResponseModel[ApiKeyResp]:
        db_api_key = api_key.get(db, id=id)
        if not db_api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found"
            )
        return ResponseModel(data=ApiKeyResp.model_validate(db_api_key))

    @staticmethod
    def get_api_keys_by_status(db: Session, status: int) -> ResponseModel[List[ApiKeyResp]]:
        items = api_key.get_multi_by_status(db, status=status)
        return ResponseModel(data=[ApiKeyResp.model_validate(item) for item in items])

    @staticmethod
    def get_api_key_page(db: Session, page: ApiKeyPageReq) -> ResponseModel[PageResult[ApiKeyResp]]:
        items, total = api_key.get_page(db, page=page)
        page_result = PageResult(
            list=[ApiKeyResp.model_validate(item) for item in items],
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        return ResponseModel(data=page_result)
