from typing import Optional
from pydantic import BaseModel, Field

class DictDataBase(BaseModel):
    sort: int = Field(..., description="排序")
    label: str = Field(..., description="字典标签")
    value: str = Field(..., description="字典键值")
    dict_type: str = Field(..., description="字典类型")
    status: int = Field(..., description="状态")
    color_type: Optional[str] = Field(None, description="颜色类型")
    css_class: Optional[str] = Field(None, description="CSS 样式")
    remark: Optional[str] = Field(None, description="备注")

class DictDataCreate(DictDataBase):
    pass

class DictDataUpdate(DictDataBase):
    id: int = Field(..., description="编号")

class DictDataResp(DictDataBase):
    id: int = Field(..., description="编号")
    creator: Optional[str] = Field(None, description="创建者")
    create_time: Optional[str] = Field(None, description="创建时间")
    updater: Optional[str] = Field(None, description="更新者")
    update_time: Optional[str] = Field(None, description="更新时间")
    deleted: Optional[bool] = Field(None, description="是否删除")

class DictDataSimpleResp(BaseModel):
    dict_type: str = Field(..., description="字典类型")
    value: str = Field(..., description="字典键值")
    label: str = Field(..., description="字典标签")
    color_type: Optional[str] = Field(None, description="颜色类型")
    css_class: Optional[str] = Field(None, description="CSS 样式")

class DictDataPageReq(BaseModel):
    label: Optional[str] = Field(None, description="字典标签")
    dict_type: Optional[str] = Field(None, description="字典类型")
    status: Optional[int] = Field(None, description="状态")
    pageNo: int = Field(1, description="页码")
    pageSize: int = Field(10, description="每页大小")
