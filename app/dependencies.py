# ============================================================
# 公共依赖Depends()
# ============================================================

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY
from app.database import SessionLocal
from app.models.user import User

# OAuth2PasswordBearer 做了两件事：
# 1. 从请求头 Authorization: Bearer <token> 里取出 token 字符串
# 2. tokenUrl="login" 告诉 /docs：去 /login 拿 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    """
    每个请求拿一个独立的数据库会话，
    请求处理完（正常 or 报错）都会自动关闭，归还连接。
    yield 之前 = 请求开始时的准备，
    yield 之后 = 请求结束后的清理。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    把 token → User 对象。
    接口只需要声明 current_user: User = Depends(get_current_user)，
    FastAPI 就会自动走完 解码→查库→返回用户 这个流程。
    token 过期/伪造/用户不存在 → 直接 401。
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="token无效")

    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user
