from app.db.session import SessionLocal
from sqlalchemy import text

def fix_model_data():
    db = SessionLocal()
    try:
        # 1. 启用 API 密钥
        db.execute(text("""
            UPDATE ai_api_key 
            SET status = 1 
            WHERE id = 27
        """))
        
        # 2. 统一平台名称为小写 - 模型
        db.execute(text("""
            UPDATE ai_model 
            SET platform = LOWER(platform) 
            WHERE id = 57
        """))
        
        # 2. 统一平台名称为小写 - API密钥
        db.execute(text("""
            UPDATE ai_api_key 
            SET platform = LOWER(platform) 
            WHERE id = 27
        """))
        
        # 3. 修正 DeepSeek 的 API URL
        db.execute(text("""
            UPDATE ai_api_key 
            SET url = 'https://api.deepseek.com/v1' 
            WHERE id = 27
        """))
        
        db.commit()
        print("✅ 数据修复完成")
        
        # 验证修改
        model = db.execute(text("SELECT * FROM ai_model WHERE id = 57")).fetchone()
        api_key = db.execute(text("SELECT * FROM ai_api_key WHERE id = 27")).fetchone()
        
        print("\n=== 修改后的模型信息 ===")
        print(f"ID: {model.id}")
        print(f"名称: {model.name}")
        print(f"平台: {model.platform}")
        print(f"状态: {model.status}")
        
        print("\n=== 修改后的API密钥信息 ===")
        print(f"ID: {api_key.id}")
        print(f"平台: {api_key.platform}")
        print(f"状态: {api_key.status}")
        print(f"URL: {api_key.url}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 修复失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_model_data()