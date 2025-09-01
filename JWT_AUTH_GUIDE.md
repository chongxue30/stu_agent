# JWT认证使用指南

## 🎯 概述

本项目已实现完整的JWT (JSON Web Token) 认证系统，所有AI聊天相关的API都需要通过JWT token进行身份验证。

## 🔐 认证流程

### 1. 用户登录获取Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "123456"
}
```

**响应示例:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "id": 1,
    "username": "admin",
    "nickname": "管理员",
    "email": "admin@example.com",
    "mobile": "",
    "avatar": "",
    "status": 0,
    "login_date": "2024-01-15T10:30:00",
    "create_time": "2024-01-15T09:00:00"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. 使用Token访问受保护的API

在所有需要认证的API请求中，在请求头中添加：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🚀 受保护的API列表

### AI聊天角色管理
- `POST /api/v1/ai/chat-role/create` - 创建聊天角色
- `PUT /api/v1/ai/chat-role/update` - 更新聊天角色
- `DELETE /api/v1/ai/chat-role/delete/{id}` - 删除聊天角色
- `GET /api/v1/ai/chat-role/get/{id}` - 获取单个角色
- `GET /api/v1/ai/chat-role/page` - 分页获取角色列表
- `GET /api/v1/ai/chat-role/category-list` - 获取角色分类

### AI聊天对话管理
- `POST /api/v1/ai/chat-conversation/create` - 创建对话
- `PUT /api/v1/ai/chat-conversation/update` - 更新对话
- `DELETE /api/v1/ai/chat-conversation/delete/{id}` - 删除对话
- `GET /api/v1/ai/chat-conversation/get/{id}` - 获取单个对话
- `GET /api/v1/ai/chat-conversation/list` - 获取对话列表
- `POST /api/v1/ai/chat-conversation/toggle-pin/{id}` - 切换置顶状态
- `GET /api/v1/ai/chat-conversation/page` - 分页获取对话列表

### AI聊天消息管理
- `POST /api/v1/ai/chat-message/send` - 发送消息
- `POST /api/v1/ai/chat-message/send-stream` - 流式发送消息
- `GET /api/v1/ai/chat-message/list/{conversation_id}` - 获取消息列表
- `DELETE /api/v1/ai/chat-message/delete/{id}` - 删除消息
- `GET /api/v1/ai/chat-message/page` - 分页获取消息列表

### API密钥管理
- `POST /api/v1/ai/api-key/create` - 创建API密钥
- `PUT /api/v1/ai/api-key/update` - 更新API密钥
- `DELETE /api/v1/ai/api-key/delete/{id}` - 删除API密钥
- `POST /api/v1/ai/api-key/restore/{id}` - 恢复API密钥
- `GET /api/v1/ai/api-key/get/{id}` - 获取单个API密钥
- `GET /api/v1/ai/api-key/simple-list` - 获取简单列表
- `GET /api/v1/ai/api-key/page` - 分页获取API密钥列表

## 🔧 前端集成示例

### JavaScript/TypeScript

```typescript
// 登录获取token
async function login(username: string, password: string) {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  
  const data = await response.json();
  if (data.code === 200) {
    // 保存token到localStorage
    localStorage.setItem('access_token', data.access_token);
    return data;
  }
  throw new Error(data.message);
}

// 使用token调用API
async function createChatRole(roleData: any) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('未登录');
  }
  
  const response = await fetch('/api/v1/ai/chat-role/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(roleData),
  });
  
  return await response.json();
}
```

### Axios

```typescript
import axios from 'axios';

// 设置请求拦截器，自动添加token
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 设置响应拦截器，处理token过期
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // token过期，跳转到登录页
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## ⚠️ 注意事项

1. **Token有效期**: 默认30分钟，过期后需要重新登录
2. **安全存储**: 建议将token存储在httpOnly cookie中，而不是localStorage
3. **自动刷新**: 可以实现token自动刷新机制
4. **错误处理**: 401状态码表示token无效或过期
5. **用户权限**: 用户只能访问和操作自己的数据

## 🔄 Token刷新机制（可选）

如果需要实现token自动刷新，可以：

1. 在响应拦截器中检测token过期
2. 使用refresh token获取新的access token
3. 自动更新存储的token
4. 重试失败的请求

## 📱 移动端集成

移动端应用同样需要在请求头中添加：

```http
Authorization: Bearer <your_jwt_token>
```

iOS (Swift):
```swift
let headers = [
    "Authorization": "Bearer \(accessToken)",
    "Content-Type": "application/json"
]
```

Android (Kotlin):
```kotlin
val headers = mapOf(
    "Authorization" to "Bearer $accessToken",
    "Content-Type" to "application/json"
)
```

现在所有AI聊天API都已经集成了JWT认证！🎉
