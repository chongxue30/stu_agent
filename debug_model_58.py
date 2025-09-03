#!/usr/bin/env python3
"""
详细调试模型ID 58 的数据类型和值
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model
from app.models.ai.api_key import ApiKey

def debug_model_58():
    db = SessionLocal()
    try:
        print("=== 详细调试模型ID 58 ===")
        model = db.query(Model).filter(Model.id == 58).first()
        if model:
            print(f"模型ID: {model.id}")
            print(f"模型名称: {model.name}")
            print(f"平台: {model.platform}")
            print(f"模型: {model.model}")
            print(f"状态: {model.status} (类型: {type(model.status)})")
            print(f"删除标记: {model.deleted} (类型: {type(model.deleted)})")
            print(f"删除标记 == False: {model.deleted == False}")
            print(f"删除标记 is False: {model.deleted is False}")
            print(f"删除标记 == 0: {model.deleted == 0}")
            print(f"API密钥ID: {model.key_id}")
            print(f"用户ID: {model.user_id}")
        else:
            print("模型ID 58 不存在")
            return

        print("\n=== 详细调试API密钥ID 28 ===")
        api_key = db.query(ApiKey).filter(ApiKey.id == 28).first()
        if api_key:
            print(f"API密钥ID: {api_key.id}")
            print(f"名称: {api_key.name}")
            print(f"平台: {api_key.platform}")
            print(f"URL: {api_key.url}")
            print(f"状态: {api_key.status} (类型: {type(api_key.status)})")
            print(f"删除标记: {api_key.deleted} (类型: {type(api_key.deleted)})")
            print(f"删除标记 == False: {api_key.deleted == False}")
            print(f"删除标记 is False: {api_key.deleted is False}")
            print(f"删除标记 == 0: {api_key.deleted == 0}")
            print(f"API密钥: {api_key.api_key[:10]}...")
        else:
            print("API密钥ID 28 不存在")

        print("\n=== 测试查询条件 ===")
        # 测试不同的查询条件
        print("1. 测试 Model.deleted.is_(False):")
        model_test1 = db.query(Model).filter(
            Model.id == 58,
            Model.deleted.is_(False)
        ).first()
        print(f"   结果: {'找到' if model_test1 else '未找到'}")

        print("2. 测试 Model.deleted == False:")
        model_test2 = db.query(Model).filter(
            Model.id == 58,
            Model.deleted == False
        ).first()
        print(f"   结果: {'找到' if model_test2 else '未找到'}")

        print("3. 测试 Model.deleted == 0:")
        model_test3 = db.query(Model).filter(
            Model.id == 58,
            Model.deleted == 0
        ).first()
        print(f"   结果: {'找到' if model_test3 else '未找到'}")

        print("4. 测试 ApiKey.deleted.is_(False):")
        api_key_test1 = db.query(ApiKey).filter(
            ApiKey.id == 28,
            ApiKey.deleted.is_(False)
        ).first()
        print(f"   结果: {'找到' if api_key_test1 else '未找到'}")

        print("5. 测试 ApiKey.deleted == False:")
        api_key_test2 = db.query(ApiKey).filter(
            ApiKey.id == 28,
            ApiKey.deleted == False
        ).first()
        print(f"   结果: {'找到' if api_key_test2 else '未找到'}")

        print("6. 测试 ApiKey.deleted == 0:")
        api_key_test3 = db.query(ApiKey).filter(
            ApiKey.id == 28,
            ApiKey.deleted == 0
        ).first()
        print(f"   结果: {'找到' if api_key_test3 else '未找到'}")

    finally:
        db.close()

if __name__ == "__main__":
    debug_model_58()

