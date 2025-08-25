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

### API 端点

- `/` - API 根路径
- `/health` - 健康检查
- `/api-info` - API 信息
- `/auth` - 认证管理
- `/ai-support` - AI 支持服务

## API 文档

启动服务器后，可以访问以下地址查看完整的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发指南

### 项目结构

```
stu_agent/
├── app/
│   ├── aiengine/        # AI 模型相关代码
│   ├── config/          # 配置文件
│   ├── models/          # 数据库模型
│   ├── routes/          # API 路由
│   ├── schemas/         # Pydantic 模型
│   ├── services/        # 业务逻辑
│   └── utils/           # 工具函数
├── manage.py            # 项目管理脚本
└── requirements.txt     # 项目依赖
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