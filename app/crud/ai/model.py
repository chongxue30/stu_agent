from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.ai.model import Model
from app.schemas.ai.model import ModelCreate, ModelUpdate, ModelPageReq

class CRUDModel(CRUDBase[Model, ModelCreate, ModelUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Model]:
        return db.query(Model).filter(Model.name == name, Model.deleted == 0).first()
    
    def get_multi_by_type_and_status(
        self, db: Session, *, type: int, status: Optional[int] = None
    ) -> List[Model]:
        conditions = [Model.type == type, Model.deleted == 0]
        if status is not None:
            conditions.append(Model.status == status)
        return db.query(Model).filter(and_(*conditions)).order_by(Model.sort.desc()).all()
    
    def get_page(self, db: Session, *, page: ModelPageReq) -> Tuple[List[Model], int]:
        query = db.query(Model).filter(Model.deleted == 0)
        if page.name:
            query = query.filter(Model.name.like(f"%{page.name}%"))
        if page.platform:
            query = query.filter(Model.platform == page.platform)
        if page.type is not None:
            query = query.filter(Model.type == page.type)
        if page.status is not None:
            query = query.filter(Model.status == page.status)
        
        # 添加排序
        query = query.order_by(Model.sort.desc())
        
        total = query.count()
        items = query.offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

    def soft_delete(self, db: Session, *, id: int) -> Model:
        """软删除模型"""
        return self.soft_remove(db, id=id)

model = CRUDModel(Model)
