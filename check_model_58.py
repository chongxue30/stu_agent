#!/usr/bin/env python3
"""
检查模型ID 58 和 API key 28 的配置情况
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model
from app.models.ai.api_key import ApiKey

def check_model_and_api_key():
    db = SessionLocal()
    try:
        print("=== 检查模型ID 58 ===")
        model = db.query(Model).filter(Model.id == 58).first()
        if model:
            print(f"模型ID: {model.id}")
            print(f"模型名称: {model.name}")
            print(f"平台: {model.platform}")
            print(f"模型: {model.model}")
            print(f"状态: {model.status}")
            print(f"删除标记: {model.deleted}")
            print(f"API密钥ID: {model.key_id}")
            print(f"用户ID: {model.user_id}")
        else:
            print("模型ID 58 不存在")
            return

        print("\n=== 检查API密钥ID 28 ===")
        api_key = db.query(ApiKey).filter(ApiKey.id == 28).first()
        if api_key:
            print(f"API密钥ID: {api_key.id}")
            print(f"名称: {api_key.name}")
            print(f"平台: {api_key.platform}")
            print(f"URL: {api_key.url}")
            print(f"状态: {api_key.status}")
            print(f"删除标记: {api_key.deleted}")
            print(f"API密钥: {api_key.api_key[:10]}...")
        else:
            print("API密钥ID 28 不存在")

        print("\n=== 检查所有可用的API密钥 ===")
        all_api_keys = db.query(ApiKey).filter(
            ApiKey.status == 1,
            ApiKey.deleted.is_(False)
        ).all()
        print(f"找到 {len(all_api_keys)} 个可用的API密钥:")
        for ak in all_api_keys:
            print(f"  ID: {ak.id}, 名称: {ak.name}, 平台: {ak.platform}, URL: {ak.url}")

        print("\n=== 检查所有可用的模型 ===")
        all_models = db.query(Model).filter(
            Model.status == 1,
            Model.deleted.is_(False)
        ).all()
        print(f"找到 {len(all_models)} 个可用的模型:")
        for m in all_models:
            print(f"  ID: {m.id}, 名称: {m.name}, 平台: {m.platform}, 模型: {m.model}, API密钥ID: {m.key_id}")

    finally:
        db.close()

if __name__ == "__main__":
    check_model_and_api_key()

