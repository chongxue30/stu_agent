from typing import List, Optional, Tuple
import json
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.ai.chat_role import ChatRole
from app.schemas.ai.chat_role import ChatRoleCreate, ChatRoleUpdate, ChatRolePageReq

class CRUDChatRole(CRUDBase[ChatRole, ChatRoleCreate, ChatRoleUpdate]):
    def _prepare_create_data(self, obj_in):
        """准备创建数据，将列表转换为JSON字符串"""
        data = super()._prepare_create_data(obj_in)
        # 将布尔值转换为整数
        if "public_status" in data:
            data["public_status"] = 1 if data["public_status"] else 0
        if "deleted" in data:
            data["deleted"] = 1 if data["deleted"] else 0
        # 将列表转换为JSON字符串
        if "knowledge_ids" in data:
            data["knowledge_ids"] = json.dumps(data["knowledge_ids"] or [])
        if "tool_ids" in data:
            data["tool_ids"] = json.dumps(data["tool_ids"] or [])
        return data

    def _prepare_update_data(self, obj_in):
        """准备更新数据，将列表转换为JSON字符串"""
        data = super()._prepare_update_data(obj_in)
        if "knowledge_ids" in data:
            data["knowledge_ids"] = json.dumps(data["knowledge_ids"] or [])
        if "tool_ids" in data:
            data["tool_ids"] = json.dumps(data["tool_ids"] or [])
        return data

    def get_by_name_and_user(self, db: Session, *, name: str, user_id: Optional[int]) -> Optional[ChatRole]:
        query = db.query(ChatRole).filter(ChatRole.name == name, ChatRole.deleted == 0)
        if user_id is not None:
            query = query.filter(ChatRole.user_id == user_id)
        return query.first()
    
    def get_category_list(self, db: Session) -> List[str]:
        return [item[0] for item in db.query(ChatRole.category).distinct().filter(ChatRole.deleted == 0).all() if item[0]]
    
    def get_page(self, db: Session, *, page: ChatRolePageReq) -> Tuple[List[ChatRole], int]:
        query = db.query(ChatRole).filter(ChatRole.deleted == 0)
        if page.name:
            query = query.filter(ChatRole.name.like(f"%{page.name}%"))
        if page.category:
            query = query.filter(ChatRole.category == page.category)
        if page.public_status is not None:
            query = query.filter(ChatRole.public_status == page.public_status)
        if page.status is not None:
            query = query.filter(ChatRole.status == page.status)
        
        total = query.count()
        items = query.order_by(ChatRole.sort).offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

    def soft_delete(self, db: Session, *, id: int) -> ChatRole:
        """软删除聊天角色"""
        return self.soft_remove(db, id=id)

chat_role = CRUDChatRole(ChatRole)
