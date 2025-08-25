from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
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
    db: Session = Depends(get_db)
):
    """
    创建 AI 模型
    """
    return ModelService.create_model(db=db, model_in=model_in)

@router.put("/update", response_model=ResponseModel[ModelResp])
def update_model(
    model_in: ModelUpdate,
    db: Session = Depends(get_db)
):
    """
    更新 AI 模型
    """
    return ModelService.update_model(db=db, model_in=model_in)

@router.delete("/delete/{id}", response_model=ResponseModel[ModelResp])
def delete_model(
    id: int,
    db: Session = Depends(get_db)
):
    """
    删除 AI 模型
    """
    return ModelService.delete_model(db=db, id=id)

@router.get("/get/{id}", response_model=ResponseModel[ModelResp])
def get_model(
    id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个 AI 模型
    """
    return ModelService.get_model(db=db, id=id)

@router.get("/simple-list", response_model=ResponseModel[List[ModelResp]])
def get_simple_list(
    type: int,
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取简单 AI 模型列表
    """
    return ModelService.get_models_by_type(db=db, type=type, status=status)

@router.get("/page", response_model=ResponseModel[PageResult[ModelResp]])
def get_model_page(
    page: ModelPageReq = Depends(),
    db: Session = Depends(get_db)
):
    """
    获取 AI 模型分页列表
    """
    return ModelService.get_model_page(db=db, page=page)
