# ============================================================
# 博客系统后端 — 入口文件
# 创建 FastAPI 应用、注册子路由、启动时自动建表
# ============================================================

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import auth, posts

app = FastAPI()

# 启动时检查，表不存在就根据 models 定义自动建表
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    """首页重定向到静态页面"""
    return RedirectResponse(url="/static/index.html")


# 把 auth.py 和 posts.py 里定义的路由注册到大 app 上
app.include_router(auth.router)
app.include_router(posts.router)

# 挂载静态文件目录，/static/xxx → static/ 文件夹下的文件
# 必须放在 include_router 之后，否则会拦截所有路由
app.mount("/static", StaticFiles(directory="static"), name="static")
