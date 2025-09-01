from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel, Field
from datetime import datetime

DataT = TypeVar("DataT")

class ResponseModel(BaseModel, Generic[DataT]):
    code: int = 0
    data: Optional[DataT] = None
    msg: str = "success"

class PageParam(BaseModel):
    pageNo: int = 1
    pageSize: int = 10

class PageResult(BaseModel, Generic[DataT]):
    list: List[DataT]
    total: int
    pageNo: int
    pageSize: int

class BaseResp(BaseModel):
    id: int
    creator: Optional[str] = None
    create_time: Optional[datetime] = None
    updater: Optional[str] = None
    update_time: Optional[datetime] = None
    deleted: bool = False
    tenant_id: Optional[int] = Field(0, description="租户编号")

    class Config:
        from_attributes = True
