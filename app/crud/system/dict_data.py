from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.system.dict_data import DictData
from app.schemas.system.dict_data import DictDataCreate, DictDataUpdate, DictDataPageReq

class CRUDDictData(CRUDBase[DictData, DictDataCreate, DictDataUpdate]):
    def get_by_dict_type_and_value(self, db: Session, *, dict_type: str, value: str) -> Optional[DictData]:
        return db.query(DictData).filter(DictData.dict_type == dict_type, DictData.value == value, DictData.deleted == 0).first()
    
    def get_by_dict_type_and_label(self, db: Session, *, dict_type: str, label: str) -> Optional[DictData]:
        return db.query(DictData).filter(DictData.dict_type == dict_type, DictData.label == label, DictData.deleted == 0).first()
    
    def get_multi_by_dict_type(self, db: Session, *, dict_type: str) -> List[DictData]:
        return db.query(DictData).filter(DictData.dict_type == dict_type, DictData.deleted == 0).order_by(DictData.sort).all()
    
    def get_multi_by_status(self, db: Session, *, status: int) -> List[DictData]:
        return db.query(DictData).filter(DictData.status == status, DictData.deleted == 0).all()
    
    def get_page(self, db: Session, *, page: DictDataPageReq) -> Tuple[List[DictData], int]:
        query = db.query(DictData).filter(DictData.deleted == 0)
        if page.label:
            query = query.filter(DictData.label.like(f"%{page.label}%"))
        if page.dict_type:
            query = query.filter(DictData.dict_type == page.dict_type)
        if page.status is not None:
            query = query.filter(DictData.status == page.status)
        
        total = query.count()
        items = query.order_by(DictData.dict_type, DictData.sort).offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

dict_data = CRUDDictData(DictData)
