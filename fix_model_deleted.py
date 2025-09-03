#!/usr/bin/env python3
"""
只修复模型ID 58 的删除标记
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model

def fix_model_deleted():
    db = SessionLocal()
    try:
        print("=== 修复模型ID 58 的删除标记 ===")
        model = db.query(Model).filter(Model.id == 58).first()
        if model:
            print(f"修复前 - 删除标记: {model.deleted}")
            model.deleted = False  # 设置为未删除
            db.commit()
            print(f"修复后 - 删除标记: {model.deleted}")
            print("✅ 模型ID 58 删除标记修复成功")
        else:
            print("❌ 模型ID 58 不存在")

    except Exception as e:
        print(f"修复过程中出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_model_deleted()

