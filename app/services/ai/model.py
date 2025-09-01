from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.ai.model import model
from app.crud.ai.api_key import api_key
from app.schemas.ai.model import ModelCreate, ModelUpdate, ModelPageReq, ModelResp
from app.schemas.common.response import PageResult, ResponseModel
from app.models.ai.model import Model

class ModelService:
    @staticmethod
    def create_model(db: Session, model_in: ModelCreate, user_id: int) -> ResponseModel[ModelResp]:
        # 设置当前用户ID
        model_in.user_id = user_id
        
        # 检查名称是否已存在（对于同一用户）
        db_model = model.get_by_name_and_user(db, name=model_in.name, user_id=user_id)
        if db_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model name already exists"
            )
        
        # 检查 API 密钥是否存在且属于当前用户
        db_api_key = api_key.get(db, id=model_in.key_id)
        if not db_api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found"
            )
        if db_api_key.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API Key does not belong to current user"
            )
        
        db_obj = model.create(db, obj_in=model_in)
        return ResponseModel(data=ModelResp.model_validate(db_obj))

    @staticmethod
    def update_model(db: Session, model_in: ModelUpdate, user_id: int) -> ResponseModel[ModelResp]:
        # 检查是否存在
        db_model = model.get(db, id=model_in.id)
        if not db_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model not found"
            )
        
        # 检查模型是否属于当前用户
        if db_model.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Model does not belong to current user"
            )
        
        # 检查名称是否已存在（排除自己，对于同一用户）
        name_exists = model.get_by_name_and_user(db, name=model_in.name, user_id=user_id)
        if name_exists and name_exists.id != model_in.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model name already exists"
            )
        
        # 检查 API 密钥是否存在且属于当前用户
        db_api_key = api_key.get(db, id=model_in.key_id)
        if not db_api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API Key not found"
            )
        if db_api_key.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API Key does not belong to current user"
            )
        
        db_obj = model.update(db, db_obj=db_model, obj_in=model_in)
        return ResponseModel(data=ModelResp.model_validate(db_obj))

    @staticmethod
    def delete_model(db: Session, id: int, user_id: int) -> ResponseModel[ModelResp]:
        db_model = model.get(db, id=id)
        if not db_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model not found"
            )
        
        # 检查模型是否属于当前用户
        if db_model.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Model does not belong to current user"
            )
        
        db_obj = model.soft_delete(db, id=id)
        return ResponseModel(data=ModelResp.model_validate(db_obj))

    @staticmethod
    def get_model(db: Session, id: int, user_id: int) -> ResponseModel[ModelResp]:
        db_model = model.get(db, id=id)
        if not db_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model not found"
            )
        
        # 检查模型是否属于当前用户
        if db_model.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Model does not belong to current user"
            )
        
        # 构建响应，包含 API 密钥信息
        model_resp = ModelResp.model_validate(db_model)
        model_resp.api_key_name = db_model.api_key.name if db_model.api_key else None
        return ResponseModel(data=model_resp)

    @staticmethod
    def get_models_by_type(
        db: Session, type: int, status: Optional[int] = None, user_id: int = None
    ) -> ResponseModel[List[ModelResp]]:
        models = model.get_multi_by_type_and_status(db, type=type, status=status, user_id=user_id)
        # 构建响应列表，包含 API 密钥信息
        model_resps = []
        for m in models:
            model_resp = ModelResp.model_validate(m)
            model_resp.api_key_name = m.api_key.name if m.api_key else None
            model_resps.append(model_resp)
        return ResponseModel(data=model_resps)

    @staticmethod
    def get_model_page(db: Session, page: ModelPageReq, user_id: int) -> ResponseModel[PageResult[ModelResp]]:
        items, total = model.get_page(db, page=page, user_id=user_id)
        # 构建响应列表，包含 API 密钥信息
        model_resps = []
        for m in items:
            model_resp = ModelResp.model_validate(m)
            model_resp.api_key_name = m.api_key.name if m.api_key else None
            model_resps.append(model_resp)
            
        page_result = PageResult(
            list=model_resps,
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        return ResponseModel(data=page_result)
