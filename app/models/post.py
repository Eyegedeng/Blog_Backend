# ============================================================
# Post ORM 模型 — 对应 MySQL 里的 posts 表
# ============================================================

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)                                # 主键、自增
    title = Column(String(100), nullable=False)                           # 标题、不为空
    content = Column(String(500), nullable=False)                         # 正文、不为空
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)   # 外键 → users 表
