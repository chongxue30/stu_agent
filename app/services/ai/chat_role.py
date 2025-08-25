from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.ai.chat_role import chat_role
from app.crud.ai.model import model
from app.schemas.ai.chat_role import ChatRoleCreate, ChatRoleUpdate, ChatRolePageReq, ChatRoleResp, ChatRoleResp
from app.schemas.common.response import PageResult, ResponseModel
from app.models.ai.chat_role import ChatRole

class ChatRoleService:
    @staticmethod
    def create_chat_role(db: Session, role_in: ChatRoleCreate) -> ResponseModel[ChatRoleResp]:
        # 检查名称是否已存在（对于同一用户）
        db_role = chat_role.get_by_name_and_user(db, name=role_in.name, user_id=role_in.user_id)
        if db_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat role name already exists"
            )
        
        # 如果指定了模型，检查模型是否存在
        if role_in.model_id:
            db_model = model.get(db, id=role_in.model_id)
            if not db_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Model not found"
                )
        
        db_obj = chat_role.create(db, obj_in=role_in)
        return ResponseModel(data=ChatRoleResp.model_validate(db_obj))

    @staticmethod
    def update_chat_role(db: Session, role_in: ChatRoleUpdate) -> ResponseModel[ChatRoleResp]:
        # 检查是否存在
        db_role = chat_role.get(db, id=role_in.id)
        if not db_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat role not found"
            )
        
        # 检查名称是否已存在（对于同一用户，排除自己）
        name_exists = chat_role.get_by_name_and_user(db, name=role_in.name, user_id=role_in.user_id)
        if name_exists and name_exists.id != role_in.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat role name already exists"
            )
        
        # 如果指定了模型，检查模型是否存在
        if role_in.model_id:
            db_model = model.get(db, id=role_in.model_id)
            if not db_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Model not found"
                )
        
        db_obj = chat_role.update(db, db_obj=db_role, obj_in=role_in)
        return ResponseModel(data=ChatRoleResp.model_validate(db_obj))

    @staticmethod
    def delete_chat_role(db: Session, id: int) -> ResponseModel[ChatRoleResp]:
        db_role = chat_role.get(db, id=id)
        if not db_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat role not found"
            )
        db_obj = chat_role.remove(db, id=id)
        return ResponseModel(data=ChatRoleResp.model_validate(db_obj))

    @staticmethod
    def get_chat_role(db: Session, id: int) -> ResponseModel[ChatRoleResp]:
        db_role = chat_role.get(db, id=id)
        if not db_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat role not found"
            )
        
        # 构建响应，包含模型信息
        role_resp = ChatRoleResp.model_validate(db_role)
        role_resp.model_name = db_role.model.name if db_role.model else None
        return ResponseModel(data=role_resp)

    @staticmethod
    def get_categories(db: Session) -> ResponseModel[List[str]]:
        """获取所有角色分类"""
        return ResponseModel(data=chat_role.get_categories(db))

    @staticmethod
    def get_chat_role_page(db: Session, page: ChatRolePageReq) -> ResponseModel[PageResult[ChatRoleResp]]:
        items, total = chat_role.get_page(db, page=page)
        
        # 构建响应列表，包含模型信息
        role_resps = []
        for r in items:
            role_resp = ChatRoleResp.model_validate(r)
            role_resp.model_name = r.model.name if r.model else None
            role_resps.append(role_resp)
            
        page_result = PageResult(
            list=role_resps,
            total=total,
            pageNo=page.pageNo,
            pageSize=page.pageSize
        )
        return ResponseModel(data=page_result)
