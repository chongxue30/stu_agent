#!/usr/bin/env python3
"""
修复模型ID 58 和 API密钥ID 28 的配置
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model
from app.models.ai.api_key import ApiKey

def fix_model_and_api_key():
    db = SessionLocal()
    try:
        print("=== 修复API密钥ID 28 ===")
        # 修复API密钥状态和删除标记
        api_key = db.query(ApiKey).filter(ApiKey.id == 28).first()
        if api_key:
            print(f"修复前 - 状态: {api_key.status}, 删除标记: {api_key.deleted}")
            api_key.status = 1  # 启用
            api_key.deleted = False  # 未删除
            db.commit()
            print(f"修复后 - 状态: {api_key.status}, 删除标记: {api_key.deleted}")
        else:
            print("API密钥ID 28 不存在")

        print("\n=== 修复模型ID 58 ===")
        # 修复模型删除标记
        model = db.query(Model).filter(Model.id == 58).first()
        if model:
            print(f"修复前 - 删除标记: {model.deleted}")
            model.deleted = False  # 未删除
            db.commit()
            print(f"修复后 - 删除标记: {model.deleted}")
        else:
            print("模型ID 58 不存在")

        print("\n=== 验证修复结果 ===")
        # 验证API密钥
        api_key_check = db.query(ApiKey).filter(
            ApiKey.id == 28,
            ApiKey.status == 1,
            ApiKey.deleted.is_(False)
        ).first()
        if api_key_check:
            print("✅ API密钥ID 28 修复成功")
        else:
            print("❌ API密钥ID 28 修复失败")

        # 验证模型
        model_check = db.query(Model).filter(
            Model.id == 58,
            Model.status == 1,
            Model.deleted.is_(False)
        ).first()
        if model_check:
            print("✅ 模型ID 58 修复成功")
        else:
            print("❌ 模型ID 58 修复失败")

    except Exception as e:
        print(f"修复过程中出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_model_and_api_key()

