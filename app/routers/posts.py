# ============================================================
# 文章路由：CRUD
# 除了 GET 不需要登录，创建/更新/删除都要验证身份 + 权限
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostOut

router = APIRouter()


@router.get("/posts", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db)):
    """
    获取所有文章（含作者名），不需要登录。
    用 JOIN 关联 users 表拿到 username。
    """
    stmt = select(Post, User.username).join(User, Post.author_id == User.id)
    results = db.execute(stmt).all()
    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_name": username,
        }
        for post, username in results
    ]


@router.post("/posts")
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建文章，需要登录。
    author_id 直接从 current_user 拿，客户端不用传，也不能伪造。
    """
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_user.id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/posts/{post_id}")
def update_post(
    post_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新文章，需要登录 + 作者本人。
    两层检查：404（文章不存在）→ 403（不是作者）。
    """
    stmt = select(Post).where(Post.id == post_id)
    post = db.execute(stmt).scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改他人文章")

    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除文章，需要登录 + 作者本人。
    和更新同样的两层检查，只是最后调的是 db.delete 而不是改字段。
    """
    stmt = select(Post).where(Post.id == post_id)
    post = db.execute(stmt).scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除他人文章")

    db.delete(post)
    db.commit()
    return {"msg": f"文章{post_id}删除成功"}
