# ============================================================
# 配置文件放全局常量
# ============================================================

SECRET_KEY = "your-secret-key-change-this-to-random-string"  # JWT 签名密钥
ALGORITHM = "HS256"                                          # JWT 签名算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30                             # token 有效期（分钟）
