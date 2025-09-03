#!/usr/bin/env python3
"""
测试 ModelFactory 的查询逻辑
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.engine.model import ModelFactory

def test_model_factory():
    db = SessionLocal()
    try:
        print("=== 测试 ModelFactory.create_model_by_id ===")
        
        # 测试创建模型实例
        try:
            model = ModelFactory.create_model_by_id(db, model_id=58, user_id=142)
            print("✅ 模型创建成功!")
            print(f"模型类型: {type(model)}")
            print(f"模型名称: {model.model_name}")
            print(f"API基础URL: {model.openai_api_base}")
        except Exception as e:
            print(f"❌ 模型创建失败: {e}")
            import traceback
            traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    test_model_factory()

