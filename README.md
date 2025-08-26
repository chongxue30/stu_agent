# AI Support API

这是一个基于 FastAPI 构建的 AI 支持服务 API，提供用户认证和 AI 聊天功能。

## 功能特点

- 用户认证和授权
- AI 聊天支持
- 支持多种 AI 模型（智谱 AI、DeepSeek 等）
- RESTful API 设计
- 完整的 API 文档

## 技术栈

- Python 3.9+
- FastAPI
- SQLAlchemy
- MySQL
- LangChain
- Various AI Models (智谱 AI, DeepSeek)

## 快速开始

### 环境要求

- Python 3.9 或更高版本
- MySQL 数据库
- 虚拟环境（推荐）

### 安装步骤

1. 克隆项目并创建虚拟环境：
```bash
git clone [repository_url]
cd stu_agent
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建 `.env` 文件并设置以下变量：
```env
DATABASE_HOST=your_db_host
DATABASE_PORT=3306
DATABASE_NAME=stu_agent
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password

# AI Model Settings
MODEL_NAME=your_model_name
MODEL_API_KEY=your_api_key
```

4. 初始化数据库：
```bash
python manage.py initdb
```

5. 启动服务器：
```bash
python manage.py runserver
```

服务器将在 http://localhost:8000 启动

## 项目管理命令

### 使用 manage.py 脚本

项目提供了 `manage.py` 脚本来管理各种操作：

#### 启动服务器
```bash
# 默认端口 8000
python manage.py runserver

# 自定义端口
python manage.py runserver 8001
python manage.py runserver 8002
```

#### 数据库管理
```bash
# 初始化数据库（创建表和默认用户）
python manage.py initdb

# 仅创建数据库表
python manage.py createtables
```

#### 其他命令
```bash
# 运行测试
python manage.py test

# 检查依赖
python manage.py deps

# 显示帮助
python manage.py help
```

### 直接启动方式

除了使用 `manage.py`，也可以直接启动：

#### 方式1：使用 uvicorn 直接启动
```bash
# 激活虚拟环境
source .venv/bin/activate

# 直接启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 方式2：使用 Python 模块启动
```bash
# 激活虚拟环境
source .venv/bin/activate

# 模块方式启动
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 环境变量配置

#### 数据库配置
```bash
export DATABASE_HOST="rm-bp18ni4370md7m57dzo.mysql.rds.aliyuncs.com"
export DATABASE_PORT=3306
export DATABASE_NAME="stu_agent"
export DATABASE_USER="root"
export DATABASE_PASSWORD="your_password"
```

#### AI 模型配置
```bash
export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
export MODEL_API_KEY="your-zhipu-api-key"
export MODEL_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"
```

### 常用启动组合

#### 开发环境启动
```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 检查依赖
python manage.py deps

# 3. 启动服务器（端口8000）
python manage.py runserver
```

#### 生产环境启动
```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 直接启动（无热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 调试模式启动
```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 启动服务器（端口8001，便于调试）
python manage.py runserver 8001
```

### API 端点

#### 基础接口
- `/api/v1/health` - 健康检查

#### 认证管理
- `/api/v1/auth/login` - 用户登录
- `/api/v1/auth/register` - 用户注册
- `/api/v1/auth/profile/{user_id}` - 获取用户信息
- `/api/v1/auth/create-admin` - 创建默认管理员

#### AI 管理
- `/api/v1/ai/api-key/*` - API 密钥管理
- `/api/v1/ai/model/*` - AI 模型管理
- `/api/v1/ai/chat-role/*` - 聊天角色管理

#### 完整 API 文档
启动服务器后，可以访问以下地址查看完整的 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 文档

启动服务器后，可以访问以下地址查看完整的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发指南

### 项目结构

```
stu_agent/
├── app/
│   ├── api/             # API 路由层
│   │   ├── v1/          # API 版本1
│   │   │   ├── endpoints/  # 具体端点
│   │   │   │   ├── auth.py      # 认证接口
│   │   │   │   ├── ai/          # AI 相关接口
│   │   │   │   │   ├── api_key.py    # API 密钥管理
│   │   │   │   │   ├── model.py      # 模型管理
│   │   │   │   │   └── chat_role.py  # 聊天角色管理
│   │   │   └── ai/          # AI 模型引擎
│   │   └── api.py       # 主路由配置
│   ├── core/            # 核心配置
│   │   ├── config.py    # 应用配置
│   │   └── security.py  # 安全相关
│   ├── crud/            # 数据库操作
│   ├── db/              # 数据库配置
│   ├── models/          # 数据库模型
│   ├── schemas/         # Pydantic 模型
│   ├── services/        # 业务逻辑
│   └── utils/           # 工具函数
├── manage.py            # 项目管理脚本
├── requirements.txt     # 项目依赖
└── alembic.ini         # 数据库迁移配置
```

### 添加新功能

1. 在 `models` 目录中定义数据模型
2. 在 `schemas` 目录中创建相应的 Pydantic 模型
3. 在 `services` 目录中实现业务逻辑
4. 在 `routes` 目录中添加新的路由
5. 在 `app.py` 中注册新的路由

## 许可证

[Your License]

## 联系方式

[Your Contact Information]