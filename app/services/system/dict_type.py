from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.system.dict_type import dict_type
from app.schemas.system.dict_type import DictTypeCreate, DictTypeUpdate, DictTypePageReq, DictTypeResp
from app.schemas.common.response import PageResult, ResponseModel

class DictTypeService:
    @staticmethod
    def create_dict_type(db: Session, dict_type_in: DictTypeCreate) -> ResponseModel[int]:
        # 检查类型是否已存在
        db_dict_type = dict_type.get_by_type(db, type=dict_type_in.type)
        if db_dict_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="字典类型已存在"
            )
        
        db_obj = dict_type.create(db, obj_in=dict_type_in)
        return ResponseModel(data=db_obj.id)

    @staticmethod
    def update_dict_type(db: Session, dict_type_in: DictTypeUpdate) -> ResponseModel[bool]:
        # 检查是否存在
        db_dict_type = dict_type.get(db, id=dict_type_in.id)
        if not db_dict_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典类型不存在"
            )
        
        # 检查类型是否已存在（排除自己）
        type_exists = dict_type.get_by_type(db, type=dict_type_in.type)
        if type_exists and type_exists.id != dict_type_in.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="字典类型已存在"
            )
        
        dict_type.update(db, db_obj=db_dict_type, obj_in=dict_type_in)
        return ResponseModel(data=True)

    @staticmethod
    def delete_dict_type(db: Session, id: int) -> ResponseModel[bool]:
        db_dict_type = dict_type.get(db, id=id)
        if not db_dict_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典类型不存在"
            )
        
        # 使用软删除
        dict_type.soft_remove(db, id=id)
        return ResponseModel(data=True)

    @staticmethod
    def get_dict_type(db: Session, id: int) -> ResponseModel[DictTypeResp]:
        db_dict_type = dict_type.get(db, id=id)
        if not db_dict_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="字典类型不存在"
            )
        return ResponseModel(data=DictTypeResp.model_validate(db_dict_type))

    @staticmethod
    def get_dict_type_page(db: Session, page: DictTypePageReq) -> ResponseModel[PageResult[DictTypeResp]]:
        items, total = dict_type.get_page(db, page=page)
        page_result = PageResult(
            list=[DictTypeResp.model_validate(item) for item in items],
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        return ResponseModel(data=page_result)

    @staticmethod
    def get_dict_type_by_type(db: Session, type: str) -> ResponseModel[Optional[DictTypeResp]]:
        db_dict_type = dict_type.get_by_type(db, type=type)
        if db_dict_type:
            return ResponseModel(data=DictTypeResp.model_validate(db_dict_type))
        return ResponseModel(data=None)
