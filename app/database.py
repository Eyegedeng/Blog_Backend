# ============================================================
# 数据库连接
# 创建引擎 + 会话工厂 + ORM 基类，其他文件从这里 import
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# "mysql+pymysql://用户名:密码@地址/数据库名"
DATABASE_URL = "mysql+pymysql://root:123456@localhost/blog"

engine = create_engine(DATABASE_URL)          # 引擎：负责和 MySQL 通信
SessionLocal = sessionmaker(bind=engine)      # 会话工厂：每次请求调它拿会话
Base = declarative_base()                     # ORM 基类：所有 model 都继承它
