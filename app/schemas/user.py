# ============================================================
# User 的 Pydantic 模型（schema）
# 注册时客户端发用户名 + 密码
# ============================================================

from pydantic import BaseModel


class UserCreate(BaseModel):
    """注册请求体：用户名 + 明文密码"""
    username: str
    password: str
