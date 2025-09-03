from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import Base
from app.schemas.common.response import PageParam

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """获取单个记录（排除已删除的）"""
        query = db.query(self.model).filter(self.model.id == id)
        # 如果模型有 deleted 字段，则过滤掉已删除的记录
        if hasattr(self.model, 'deleted'):
            query = query.filter(self.model.deleted == 0)
        return query.first()

    def get_multi(
        self, db: Session, *, page: PageParam
    ) -> tuple[List[ModelType], int]:
        """获取分页记录（排除已删除的）"""
        query = db.query(self.model)
        # 如果模型有 deleted 字段，则过滤掉已删除的记录
        if hasattr(self.model, 'deleted'):
            query = query.filter(self.model.deleted == 0)
        total = query.count()
        items = query.offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

    def _prepare_create_data(self, obj_in: CreateSchemaType) -> Dict[str, Any]:
        """准备创建数据，子类可以重写此方法以自定义数据处理"""
        return jsonable_encoder(obj_in)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = self._prepare_create_data(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """物理删除"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def soft_remove(self, db: Session, *, id: int) -> ModelType:
        """软删除 - 设置 deleted = 1"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        
        if obj and hasattr(obj, 'deleted'):
            # 使用 1 而不是 True，因为 MySQL Boolean 实际上是 TINYINT
            obj.deleted = 1
            
            if hasattr(obj, 'updater'):
                obj.updater = "system"
            
            if hasattr(obj, 'update_time'):
                from sqlalchemy.sql import func
                obj.update_time = func.now()
            
            # 强制更新 deleted 字段
            try:
                from sqlalchemy import text
                # 表名不能参数化，必须直接写在 SQL 中
                update_sql = text(f"UPDATE {obj.__tablename__} SET deleted = :deleted, updater = :updater, update_time = NOW() WHERE id = :id")
                db.execute(update_sql, {
                    'deleted': 1,
                    'updater': 'system',
                    'id': obj.id
                })
            except Exception as e:
                raise Exception(f"软删除失败: {str(e)}")
            
            db.add(obj)
            db.commit()
            db.refresh(obj)
        
        return obj
    
    def restore(self, db: Session, *, id: int) -> ModelType:
        """恢复已删除的记录 - 设置 deleted = 0"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj and hasattr(obj, 'deleted'):
            # 使用 0 而不是 False，因为 MySQL Boolean 实际上是 TINYINT
            obj.deleted = 0
            
            if hasattr(obj, 'updater'):
                obj.updater = "system"
            
            if hasattr(obj, 'update_time'):
                from sqlalchemy.sql import func
                obj.update_time = func.now()
            
            # 强制更新 deleted 字段
            try:
                from sqlalchemy import text
                # 表名不能参数化，必须直接写在 SQL 中
                update_sql = text(f"UPDATE {obj.__tablename__} SET deleted = :deleted, updater = :updater, update_time = NOW() WHERE id = :id")
                db.execute(update_sql, {
                    'deleted': 0,
                    'updater': 'system',
                    'id': obj.id
                })
            except Exception as e:
                raise Exception(f"恢复删除失败: {str(e)}")
            
            db.add(obj)
            db.commit()
            db.refresh(obj)
        
        return obj