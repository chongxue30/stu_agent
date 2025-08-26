from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.system.dict_data import dict_data
from app.schemas.system.dict_data import (
    DictDataCreate, DictDataUpdate, DictDataPageReq, DictDataResp, DictDataSimpleResp
)
from app.schemas.common.response import PageResult, ResponseModel
from typing import List

class DictDataService:
    @staticmethod
    def create_dict_data(db: Session, dict_data_in: DictDataCreate) -> ResponseModel[int]:
        # 检查字典类型和值的唯一性
        db_dict_data = dict_data.get_by_dict_type_and_value(
            db, dict_type=dict_data_in.dict_type, value=dict_data_in.value
        )
        if db_dict_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="字典数据已存在"
            )
        
        db_obj = dict_data.create(db, obj_in=dict_data_in)
        return ResponseModel(data=db_obj.id)

    @staticmethod
    def update_dict_data(db: Session, dict_data_in: DictDataUpdate) -> ResponseModel[bool]:
        # 检查是否存在
        db_dict_data = dict_data.get(db, id=dict_data_in.id)
        if not db_dict_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典数据不存在"
            )
        
        # 检查字典类型和值的唯一性（排除自己）
        value_exists = dict_data.get_by_dict_type_and_value(
            db, dict_type=dict_data_in.dict_type, value=dict_data_in.value
        )
        if value_exists and value_exists.id != dict_data_in.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="字典数据已存在"
            )
        
        dict_data.update(db, db_obj=db_dict_data, obj_in=dict_data_in)
        return ResponseModel(data=True)

    @staticmethod
    def delete_dict_data(db: Session, id: int) -> ResponseModel[bool]:
        db_dict_data = dict_data.get(db, id=id)
        if not db_dict_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典数据不存在"
            )
        
        # 使用软删除
        dict_data.soft_remove(db, id=id)
        return ResponseModel(data=True)

    @staticmethod
    def get_dict_data(db: Session, id: int) -> ResponseModel[DictDataResp]:
        db_dict_data = dict_data.get(db, id=id)
        if not db_dict_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典数据不存在"
            )
        return ResponseModel(data=DictDataResp.model_validate(db_dict_data.to_dict()))

    @staticmethod
    def get_dict_data_page(db: Session, page: DictDataPageReq) -> ResponseModel[PageResult[DictDataResp]]:
        items, total = dict_data.get_page(db, page=page)
        page_result = PageResult(
            list=[DictDataResp.model_validate(item.to_dict()) for item in items],
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        return ResponseModel(data=page_result)

    @staticmethod
    def get_dict_data_list(db: Session, dict_type: str = None) -> ResponseModel[List[DictDataSimpleResp]]:
        """获取字典数据列表（用于前端缓存）"""
        if dict_type:
            items = dict_data.get_multi_by_dict_type(db, dict_type=dict_type)
        else:
            items = dict_data.get_multi_by_status(db, status=0)  # 只查询启用状态
        
        # 将 SQLAlchemy 对象转换为字典，然后验证
        return ResponseModel(data=[DictDataSimpleResp.model_validate(item.to_dict()) for item in items])

    @staticmethod
    def get_dict_data_by_type_and_value(db: Session, dict_type: str, value: str) -> ResponseModel[DictDataResp]:
        db_dict_data = dict_data.get_by_dict_type_and_value(db, dict_type=dict_type, value=value)
        if not db_dict_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典数据不存在"
            )
        return ResponseModel(data=DictDataResp.model_validate(db_dict_data.to_dict()))
