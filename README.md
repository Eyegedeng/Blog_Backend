# 博客系统

基于 FastAPI + SQLAlchemy + MySQL 的博客后端，带前端页面，支持用户注册登录、JWT 认证、文章增删改查和权限控制。

## 技术栈

| 层级 | 技术 |
|------|------|
| 框架 | FastAPI |
| ORM | SQLAlchemy 2.0 |
| 数据库 | MySQL |
| 认证 | JWT + bcrypt + OAuth2 Password Flow |
| 前端 | 纯 HTML/CSS/JS，FastAPI 直接托管 |
| 数据校验 | Pydantic |

## 功能

- 用户注册 / 登录 / JWT 令牌签发
- 文章列表（含作者名）、创建、编辑、删除
- 权限控制：只能修改或删除自己的文章
- 前端页面：注册、登录、文章展示、弹窗编辑
- 自动生成 Swagger 文档（`/docs`）

## 项目结构

```
blog_backend/
├── app/
│   ├── main.py              # 入口：创建应用、注册路由、挂载静态文件
│   ├── config.py            # JWT 密钥、算法、过期时间
│   ├── database.py          # 数据库引擎、会话工厂、ORM 基类
│   ├── dependencies.py      # 公共依赖（get_db、get_current_user）
│   ├── models/
│   │   ├── post.py          # Post 模型
│   │   └── user.py          # User 模型
│   ├── schemas/
│   │   ├── post.py          # PostCreate、PostOut
│   │   └── user.py          # UserCreate
│   └── routers/
│       ├── auth.py          # /register、/login
│       └── posts.py         # /posts CRUD
├── static/
│   ├── index.html           # 前端页面
│   ├── style.css            # 样式
│   └── app.js               # 前端逻辑
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 创建 MySQL 数据库

```sql
CREATE DATABASE blog CHARACTER SET utf8mb4;
```

### 2. 配置数据库连接

修改 `app/database.py` 中的 `DATABASE_URL`，或在 `app/config.py` 中修改 `SECRET_KEY`。

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动

```bash
uvicorn app.main:app --reload
```

### 5. 访问

- 前端页面：http://localhost:8000
- API 文档：http://localhost:8000/docs

## API 接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/` | 跳转首页 | 无 |
| POST | `/register` | 注册 | 无 |
| POST | `/login` | 登录，返回 token | 无 |
| GET | `/posts` | 文章列表（含作者） | 无 |
| POST | `/posts` | 创建文章 | Bearer Token |
| PUT | `/posts/{id}` | 修改文章 | Bearer Token + 作者 |
| DELETE | `/posts/{id}` | 删除文章 | Bearer Token + 作者 |

## 踩坑记录

- `passlib` 和 `bcrypt 4.1+` 不兼容，需降级到 `bcrypt==4.0.1`
- `datetime.UTC` 需要 Python 3.11+，低版本用 `datetime.timezone.utc`
- bcrypt 单次哈希密码最长 72 字节，超长截断
- `fetch()` 收到 4xx/5xx 不抛异常，要手动检查 `res.ok`
- onclick 属性中单引号会破坏 HTML，需额外转义
