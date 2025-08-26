from pydantic import BaseModel, Field

class PageParam(BaseModel):
    """分页参数基类"""
    pageNo: int = Field(1, ge=1, description="页码，从1开始")
    pageSize: int = Field(10, ge=1, le=100, description="每页数量，最大100")
    
    def get_skip(self) -> int:
        """获取跳过的记录数"""
        return (self.pageNo - 1) * self.pageSize
    
    def get_limit(self) -> int:
        """获取限制的记录数"""
        return self.pageSize
