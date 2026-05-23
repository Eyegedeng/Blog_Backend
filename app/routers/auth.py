# ============================================================
# 认证路由：注册 + 登录
# 用户的入口，拿到 token 后才能调需要登录的接口
# ============================================================

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter()

# bcrypt 工具：负责 明文→哈希 和 哈希验证
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    把数据编码成 JWT token。
    data 里放了 {"sub": 用户名}，"sub" 是 JWT 标准字段，表示"这个 token 代表谁"。
    过期时间存 "exp" 字段，jwt.decode 时自动校验。
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    注册流程：
    1. 查用户名是否已存在 → 400
    2. 密码 bcrypt 哈希 → 存入数据库
    3. 返回新用户的 id 和用户名
    """
    stmt = select(User).where(User.username == user_data.username)
    existing_user = db.execute(stmt).scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # bcrypt 限制最多 72 字节，超过截断
    hashed_pwd = pwd_context.hash(user_data.password[:72])
    new_user = User(username=user_data.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 让数据库分配 id，回填到 new_user 对象
    return {"id": new_user.id, "username": new_user.username}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    登录流程：
    1. 查用户 → 验密码（verify 比的是哈希，不是明文）
    2. 通过则签发 JWT token，30分钟有效
    3. 返回 token，客户端以后每次请求带在 Authorization 头里

    OAuth2PasswordRequestForm 会把 /docs 登录表单的 username+password 解析成 form 对象。
    Depends() 空括号是因为它是一个可直接实例化的类，不需要额外函数。
    """
    stmt = select(User).where(User.username == form.username)
    user = db.execute(stmt).scalars().first()
    if not user or not pwd_context.verify(form.password[:72], user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
