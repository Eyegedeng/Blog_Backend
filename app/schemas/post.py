# ============================================================
# Post 的 Pydantic 模型（schema）
# PostCreate = 客户端发过来的请求体格式
# PostOut    = 服务端返回给客户端的响应格式
# ============================================================

from pydantic import BaseModel


class PostCreate(BaseModel):
    """创建/更新文章时，客户端要发的字段"""
    title: str
    content: str


class PostOut(BaseModel):
    """查询文章时，返回给客户端的字段"""
    id: int
    title: str
    content: str
    author_name: str  # 作者用户名，查库时从 users 表关联取

    class Config:
        from_attributes = True  # 允许从 ORM 对象直接转换（以前叫 orm_mode）
