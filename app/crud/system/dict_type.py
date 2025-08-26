from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.system.dict_type import DictType
from app.schemas.system.dict_type import DictTypeCreate, DictTypeUpdate, DictTypePageReq

class CRUDDictType(CRUDBase[DictType, DictTypeCreate, DictTypeUpdate]):
    def get_by_type(self, db: Session, *, type: str) -> Optional[DictType]:
        return db.query(DictType).filter(DictType.type == type, DictType.deleted == 0).first()
    
    def get_multi_by_status(self, db: Session, *, status: int) -> List[DictType]:
        return db.query(DictType).filter(DictType.status == status, DictType.deleted == 0).all()
    
    def get_page(self, db: Session, *, page: DictTypePageReq) -> tuple[List[DictType], int]:
        query = db.query(DictType).filter(DictType.deleted == 0)
        if page.name:
            query = query.filter(DictType.name.like(f"%{page.name}%"))
        if page.type:
            query = query.filter(DictType.type.like(f"%{page.type}%"))
        if page.status is not None:
            query = query.filter(DictType.status == page.status)
        
        total = query.count()
        items = query.offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

dict_type = CRUDDictType(DictType)
