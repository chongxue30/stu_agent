#!/usr/bin/env python
"""
FastAPI 项目管理脚本
支持启动服务器、数据库迁移、测试等命令
"""
import os
import sys
import uvicorn
from pathlib import Path

# 添加项目根目录到 Python 路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

def run_server(host="0.0.0.0", port=8000, reload=True):
    """启动 FastAPI 服务器"""
    print(f"🚀 启动服务器: http://{host}:{port}")
    print(f"📁 项目目录: {BASE_DIR}")
    print(f"🔄 热重载: {'开启' if reload else '关闭'}")
    print("按 Ctrl+C 停止服务器")
    
    uvicorn.run(
        "app.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    os.system("python -m pytest tests/ -v")

def check_dependencies():
    """检查依赖"""
    print("📦 检查依赖...")
    os.system("pip list")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python manage.py <command> [options]")
        print("\n可用命令:")
        print("  runserver    启动开发服务器")
        print("  test         运行测试")
        print("  deps         检查依赖")
        print("  help         显示帮助")
        return
    
    command = sys.argv[1]
    
    if command == "runserver":
        # 支持自定义端口: python manage.py runserver 8080
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        run_server(port=port)
    
    elif command == "test":
        run_tests()
    
    elif command == "deps":
        check_dependencies()
    
    elif command == "help":
        print("FastAPI 项目管理脚本")
        print("\n命令:")
        print("  runserver [port]  启动开发服务器 (默认端口: 8000)")
        print("  test              运行测试")
        print("  deps              检查依赖")
        print("  help              显示帮助")
    
    else:
        print(f"❌ 未知命令: {command}")
        print("使用 'python manage.py help' 查看可用命令")

if __name__ == "__main__":
    main()
