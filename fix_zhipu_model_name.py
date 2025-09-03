#!/usr/bin/env python3
"""
修复智谱AI的模型名称
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model

def fix_zhipu_model_name():
    db = SessionLocal()
    try:
        print("=== 修复智谱AI的模型名称 ===")
        
        # 查找智谱AI的模型配置
        model = db.query(Model).filter(
            Model.id == 58,
            Model.platform == "zhipu"
        ).first()
        
        if model:
            print(f"修复前模型名称: {model.model}")
            
            # 修复模型名称 - 使用智谱AI的正确模型名称
            model.model = "glm-4"  # 智谱AI的GLM-4模型
            db.commit()
            print(f"修复后模型名称: {model.model}")
            print("✅ 模型名称修复成功")
        else:
            print("❌ 未找到智谱AI的模型配置")

    except Exception as e:
        print(f"修复过程中出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_zhipu_model_name()

