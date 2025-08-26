from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.system.dict_data import DictDataService
from app.schemas.system.dict_data import (
    DictDataCreate, DictDataUpdate, DictDataResp, DictDataPageReq, DictDataSimpleResp
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List

router = APIRouter(prefix="/dict-data", tags=["字典数据管理"])

@router.post("/create", response_model=ResponseModel[int])
def create_dict_data(
    dict_data_in: DictDataCreate,
    db: Session = Depends(get_db)
):
    """创建字典数据"""
    return DictDataService.create_dict_data(db=db, dict_data_in=dict_data_in)

@router.put("/update", response_model=ResponseModel[bool])
def update_dict_data(
    dict_data_in: DictDataUpdate,
    db: Session = Depends(get_db)
):
    """更新字典数据"""
    return DictDataService.update_dict_data(db=db, dict_data_in=dict_data_in)

@router.delete("/delete/{id}", response_model=ResponseModel[bool])
def delete_dict_data(
    id: int,
    db: Session = Depends(get_db)
):
    """删除字典数据（软删除）"""
    return DictDataService.delete_dict_data(db=db, id=id)

@router.get("/get/{id}", response_model=ResponseModel[DictDataResp])
def get_dict_data(
    id: int,
    db: Session = Depends(get_db)
):
    """获取单个字典数据"""
    return DictDataService.get_dict_data(db=db, id=id)

@router.get("/page", response_model=ResponseModel[PageResult[DictDataResp]])
def get_dict_data_page(
    page: DictDataPageReq = Depends(),
    db: Session = Depends(get_db)
):
    """获取字典数据分页列表"""
    return DictDataService.get_dict_data_page(db=db, page=page)

@router.get("/simple-list", response_model=ResponseModel[List[DictDataSimpleResp]])
def get_simple_dict_data_list(
    dict_type: str = None,
    db: Session = Depends(get_db)
):
    """获得全部字典数据列表（用于前端缓存）"""
    return DictDataService.get_dict_data_list(db=db, dict_type=dict_type)

@router.get("/get-by-type-and-value", response_model=ResponseModel[DictDataResp])
def get_dict_data_by_type_and_value(
    dict_type: str,
    value: str,
    db: Session = Depends(get_db)
):
    """根据字典类型和值获取字典数据"""
    return DictDataService.get_dict_data_by_type_and_value(db=db, dict_type=dict_type, value=value)
