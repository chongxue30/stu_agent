from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.ai.api_key import ApiKey
from app.schemas.ai.api_key import ApiKeyCreate, ApiKeyUpdate, ApiKeyPageReq

class CRUDApiKey(CRUDBase[ApiKey, ApiKeyCreate, ApiKeyUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[ApiKey]:
        return db.query(ApiKey).filter(ApiKey.name == name, ApiKey.deleted == 0).first()
    
    def get_by_name_and_user(self, db: Session, *, name: str, user_id: int) -> Optional[ApiKey]:
        return db.query(ApiKey).filter(ApiKey.name == name, ApiKey.user_id == user_id, ApiKey.deleted == 0).first()
    
    def get_multi_by_status(self, db: Session, *, status: int, user_id: int) -> List[ApiKey]:
        return db.query(ApiKey).filter(ApiKey.status == status, ApiKey.user_id == user_id, ApiKey.deleted == 0).all()
    
    def get_page(self, db: Session, *, page: ApiKeyPageReq, user_id: int) -> Tuple[List[ApiKey], int]:
        query = db.query(ApiKey).filter(ApiKey.deleted == 0, ApiKey.user_id == user_id)
        if page.name:
            query = query.filter(ApiKey.name.like(f"%{page.name}%"))
        if page.platform:
            query = query.filter(ApiKey.platform == page.platform)
        if page.status is not None:
            query = query.filter(ApiKey.status == page.status)
        
        total = query.count()
        items = query.offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

    def soft_delete(self, db: Session, *, id: int) -> ApiKey:
        """软删除 API Key"""
        return self.soft_remove(db, id=id)

api_key = CRUDApiKey(ApiKey)
