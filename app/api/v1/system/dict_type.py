from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.system.dict_type import DictTypeService
from app.schemas.system.dict_type import (
    DictTypeCreate, DictTypeUpdate, DictTypeResp, DictTypePageReq
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List

router = APIRouter(prefix="/dict-type", tags=["字典类型管理"])

@router.post("/create", response_model=ResponseModel[int])
def create_dict_type(
    dict_type_in: DictTypeCreate,
    db: Session = Depends(get_db)
):
    """创建字典类型"""
    return DictTypeService.create_dict_type(db=db, dict_type_in=dict_type_in)

@router.put("/update", response_model=ResponseModel[bool])
def update_dict_type(
    dict_type_in: DictTypeUpdate,
    db: Session = Depends(get_db)
):
    """更新字典类型"""
    return DictTypeService.update_dict_type(db=db, dict_type_in=dict_type_in)

@router.delete("/delete/{id}", response_model=ResponseModel[bool])
def delete_dict_type(
    id: int,
    db: Session = Depends(get_db)
):
    """删除字典类型（软删除）"""
    return DictTypeService.delete_dict_type(db=db, id=id)

@router.get("/get/{id}", response_model=ResponseModel[DictTypeResp])
def get_dict_type(
    id: int,
    db: Session = Depends(get_db)
):
    """获取单个字典类型"""
    return DictTypeService.get_dict_type(db=db, id=id)

@router.get("/page", response_model=ResponseModel[PageResult[DictTypeResp]])
def get_dict_type_page(
    page: DictTypePageReq = Depends(),
    db: Session = Depends(get_db)
):
    """获取字典类型分页列表"""
    return DictTypeService.get_dict_type_page(db=db, page=page)

@router.get("/get-by-type/{type}", response_model=ResponseModel[DictTypeResp])
def get_dict_type_by_type(
    type: str,
    db: Session = Depends(get_db)
):
    """根据类型获取字典类型"""
    return DictTypeService.get_dict_type_by_type(db=db, type=type)
