from typing import Optional
from pydantic import BaseModel, Field

class DictTypeBase(BaseModel):
    name: str = Field(..., description="字典名称")
    type: str = Field(..., description="字典类型")
    status: int = Field(..., description="状态")
    remark: Optional[str] = Field(None, description="备注")

class DictTypeCreate(DictTypeBase):
    pass

class DictTypeUpdate(DictTypeBase):
    id: int = Field(..., description="编号")

class DictTypeResp(DictTypeBase):
    id: int = Field(..., description="编号")
    creator: Optional[str] = Field(None, description="创建者")
    create_time: Optional[str] = Field(None, description="创建时间")
    updater: Optional[str] = Field(None, description="更新者")
    update_time: Optional[str] = Field(None, description="更新时间")
    deleted: Optional[bool] = Field(None, description="是否删除")
    deleted_time: Optional[str] = Field(None, description="删除时间")

class DictTypePageReq(BaseModel):
    name: Optional[str] = Field(None, description="字典名称")
    type: Optional[str] = Field(None, description="字典类型")
    status: Optional[int] = Field(None, description="状态")
    pageNo: int = Field(1, description="页码")
    pageSize: int = Field(10, description="每页大小")
