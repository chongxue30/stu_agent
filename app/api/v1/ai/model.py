from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user_id
from app.services.ai.model import ModelService
from app.schemas.ai.model import (
    ModelCreate,
    ModelUpdate,
    ModelResp,
    ModelPageReq
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List, Optional

router = APIRouter(prefix="/model", tags=["AI模型管理"])

@router.post("/create", response_model=ResponseModel[ModelResp])
def create_model(
    model_in: ModelCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    创建 AI 模型
    """
    return ModelService.create_model(db=db, model_in=model_in, user_id=user_id)

@router.put("/update", response_model=ResponseModel[ModelResp])
def update_model(
    model_in: ModelUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    更新 AI 模型
    """
    return ModelService.update_model(db=db, model_in=model_in, user_id=user_id)

@router.delete("/delete/{id}", response_model=ResponseModel[ModelResp])
def delete_model(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    删除 AI 模型
    """
    return ModelService.delete_model(db=db, id=id, user_id=user_id)

@router.get("/get/{id}", response_model=ResponseModel[ModelResp])
def get_model(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    获取单个 AI 模型
    """
    return ModelService.get_model(db=db, id=id, user_id=user_id)

@router.get("/simple-list", response_model=ResponseModel[List[ModelResp]])
def get_simple_list(
    type: int,
    status: Optional[int] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    获取简单 AI 模型列表
    """
    return ModelService.get_models_by_type(db=db, type=type, status=status, user_id=user_id)

@router.get("/page", response_model=ResponseModel[PageResult[ModelResp]])
def get_model_page(
    page: ModelPageReq = Depends(),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    获取 AI 模型分页列表
    """
    return ModelService.get_model_page(db=db, page=page, user_id=user_id)
