from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ai.chat_message import ChatMessageService
from app.schemas.ai.chat_message import (
    ChatMessageCreate, ChatMessageUpdate, ChatMessagePageReq, ChatMessageSendReq, ChatMessageSendResp
)
from app.schemas.common.response import ResponseModel, PageResult
from typing import List
from fastapi.responses import StreamingResponse
import json

router = APIRouter(prefix="/chat-message", tags=["AI聊天消息管理"])

# 模拟用户ID（实际项目中应该从JWT token获取）
def get_current_user_id() -> int:
    # TODO: 从JWT token获取用户ID
    return 1

@router.post("/send", response_model=ResponseModel[ChatMessageSendResp])
def send_message(
    message_in: ChatMessageSendReq,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """发送消息并获取AI回复"""
    return ChatMessageService.send_message(db=db, message_in=message_in, user_id=user_id)

@router.post("/send-stream")
def send_message_stream(
    message_in: ChatMessageSendReq,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """流式发送消息并获取AI回复"""
    # 检查对话是否存在且属于当前用户
    from app.crud.ai.chat_conversation import chat_conversation
    db_conversation = chat_conversation.get(db, id=message_in.conversation_id)
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )
    
    if db_conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限在此对话中发送消息"
        )
    
    # 创建用户消息
    from app.crud.ai.chat_message import chat_message
    user_msg = chat_message.create_user_message(
        db=db,
        conversation_id=message_in.conversation_id,
        user_id=user_id,
        content=message_in.content,
        model_id=db_conversation.model_id,
        model=db_conversation.model,
        role_id=message_in.role_id
    )
    
    def generate_stream():
        try:
            from app.services.ai.chat import ChatService
            # 流式获取AI回复
            full_response = ""
            for chunk in ChatService.stream_ai_response(
                db=db,
                conversation_id=message_in.conversation_id,
                user_message=message_in.content,
                model_id=db_conversation.model_id,
                system_message=db_conversation.system_message,
                temperature=db_conversation.temperature,
                max_tokens=db_conversation.max_tokens,
                use_context=message_in.use_context,
                max_contexts=db_conversation.max_contexts
            ):
                full_response += chunk
                # 发送SSE格式的数据
                yield f"data: {json.dumps({'content': chunk, 'type': 'chunk'})}\n\n"
            
            # 创建AI回复消息
            ai_msg = chat_message.create_ai_message(
                db=db,
                conversation_id=message_in.conversation_id,
                user_id=user_id,
                content=full_response,
                model_id=db_conversation.model_id,
                model=db_conversation.model,
                reply_id=user_msg.id,
                role_id=db_conversation.role_id
            )
            
            # 发送完成信号
            yield f"data: {json.dumps({'content': '', 'type': 'done', 'message_id': ai_msg.id})}\n\n"
            
        except Exception as e:
            # 如果AI回复失败，删除用户消息
            chat_message.remove(db, id=user_msg.id)
            yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

@router.get("/list/{conversation_id}", response_model=ResponseModel[List[ChatMessageSendResp]])
def get_message_list(
    conversation_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """获取对话的消息列表"""
    return ChatMessageService.get_message_list(db=db, conversation_id=conversation_id, user_id=user_id, limit=limit)

@router.delete("/delete/{id}", response_model=ResponseModel[bool])
def delete_message(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """删除消息"""
    return ChatMessageService.delete_message(db=db, id=id, user_id=user_id)

@router.get("/page", response_model=ResponseModel[PageResult[ChatMessageSendResp]])
def get_message_page(
    page: ChatMessagePageReq = Depends(),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """分页获取消息列表"""
    return ChatMessageService.get_message_page(db=db, page=page, user_id=user_id)
