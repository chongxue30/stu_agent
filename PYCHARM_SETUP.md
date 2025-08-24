# PyCharm 配置说明

## 问题：服务器启动后 PyCharm 显示进程结束

这是因为 PyCharm 没有正确识别到后台运行的服务器进程。

## 解决方案

### 1. 检查 Python 解释器
- 转到 `File > Settings > Project > Python Interpreter`
- 确保选择了 `.venv` 虚拟环境
- 路径应该类似：`/Users/zhongchongxue/works/my_ai/stu-agent/.venv/bin/python`

### 2. 使用运行配置（推荐）
- 在 PyCharm 顶部工具栏找到运行配置下拉菜单
- 选择 "FastAPI Server"
- 点击运行按钮

### 3. 手动创建运行配置
如果 "FastAPI Server" 配置不存在：
1. 点击运行配置下拉菜单
2. 选择 "Edit Configurations..."
3. 点击 "+" 号，选择 "Python"
4. 配置如下：
   - **Name**: FastAPI Server
   - **Script path**: `$PROJECT_DIR$/manage.py`
   - **Parameters**: `runserver 8001`
   - **Working directory**: `$PROJECT_DIR$`
   - **Python interpreter**: 选择 `.venv` 环境

### 4. 验证服务器运行
配置完成后，运行 "FastAPI Server" 配置，应该能看到：
```
🚀 启动服务器: http://0.0.0.0:8001
📁 项目目录: /Users/zhongchongxue/works/my_ai/stu-agent
🔄 热重载: 开启
```

### 5. 测试 API
在浏览器中访问：`http://localhost:8001/health`

## 注意事项
- 服务器会在后台运行，PyCharm 会显示为"正在运行"状态
- 要停止服务器，点击 PyCharm 的停止按钮
- 或者使用 `Ctrl+C` 在终端中停止
