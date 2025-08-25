from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.crud.base import CRUDBase
from app.models.ai.chat_role import ChatRole
from app.schemas.ai.chat_role import ChatRoleCreate, ChatRoleUpdate, ChatRolePageReq

class CRUDChatRole(CRUDBase[ChatRole, ChatRoleCreate, ChatRoleUpdate]):
    def get_by_name_and_user(
        self, db: Session, *, name: str, user_id: Optional[int] = None
    ) -> Optional[ChatRole]:
        conditions = [ChatRole.name == name]
        if user_id is not None:
            conditions.append(ChatRole.user_id == user_id)
        return db.query(ChatRole).filter(and_(*conditions)).first()
    
    def get_categories(self, db: Session) -> List[str]:
        """获取所有角色分类"""
        categories = db.query(ChatRole.category).distinct().all()
        return [c[0] for c in categories if c[0]]  # 过滤掉 None
    
    def get_page(self, db: Session, *, page: ChatRolePageReq) -> Tuple[List[ChatRole], int]:
        query = db.query(ChatRole)
        
        # 构建查询条件
        if page.name:
            query = query.filter(ChatRole.name.like(f"%{page.name}%"))
        if page.category:
            query = query.filter(ChatRole.category == page.category)
        if page.public_status is not None:
            query = query.filter(ChatRole.public_status == page.public_status)
        if page.status is not None:
            query = query.filter(ChatRole.status == page.status)
        if page.user_id is not None:
            query = query.filter(ChatRole.user_id == page.user_id)
        
        # 添加排序
        query = query.order_by(ChatRole.sort.desc(), ChatRole.id.desc())
        
        total = query.count()
        items = query.offset((page.pageNo - 1) * page.pageSize).limit(page.pageSize).all()
        return items, total

chat_role = CRUDChatRole(ChatRole)
