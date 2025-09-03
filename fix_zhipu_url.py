#!/usr/bin/env python3
"""
修复智谱AI的URL配置
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.api_key import ApiKey

def fix_zhipu_url():
    db = SessionLocal()
    try:
        print("=== 修复智谱AI的URL配置 ===")
        
        # 查找智谱AI的API密钥
        api_key = db.query(ApiKey).filter(
            ApiKey.id == 28,
            ApiKey.platform == "zhipu"
        ).first()
        
        if api_key:
            print(f"修复前URL: {api_key.url}")
            
            # 修复URL - 移除重复的 /chat/completions 路径
            if api_key.url.endswith("/chat/completions"):
                new_url = api_key.url.replace("/chat/completions", "")
                api_key.url = new_url
                db.commit()
                print(f"修复后URL: {api_key.url}")
                print("✅ URL修复成功")
            else:
                print("URL格式正确，无需修复")
        else:
            print("❌ 未找到智谱AI的API密钥配置")

    except Exception as e:
        print(f"修复过程中出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_zhipu_url()

