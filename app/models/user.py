# ============================================================
# User ORM 模型 — 对应 MySQL 里的 users 表
# ============================================================

from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)                # 主键、自增、加索引
    username = Column(String(50), unique=True, index=True, nullable=False)  # 唯一、索引、不为空
    hashed_password = Column(String(128), nullable=False)             # bcrypt 哈希，不存明文
