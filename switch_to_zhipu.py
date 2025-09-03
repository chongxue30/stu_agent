from app.db.session import SessionLocal
from sqlalchemy import text

def switch_to_zhipu():
    db = SessionLocal()
    try:
        # 1. 更新模型配置为智谱
        db.execute(text("""
            UPDATE ai_model 
            SET 
                platform = 'zhipu',
                model = 'glm-4',
                name = '智谱GLM-4'
            WHERE id = 57
        """))
        
        # 2. 更新API密钥配置为智谱
        db.execute(text("""
            UPDATE ai_api_key 
            SET 
                platform = 'zhipu',
                name = '智谱AI密钥',
                url = 'https://open.bigmodel.cn/api/paas/v4'
            WHERE id = 27
        """))
        
        db.commit()
        print("✅ 已切换到智谱大模型")
        
        # 验证修改
        model = db.execute(text("SELECT * FROM ai_model WHERE id = 57")).fetchone()
        api_key = db.execute(text("SELECT * FROM ai_api_key WHERE id = 27")).fetchone()
        
        print("\n=== 修改后的模型信息 ===")
        print(f"ID: {model.id}")
        print(f"名称: {model.name}")
        print(f"平台: {model.platform}")
        print(f"模型标识: {model.model}")
        print(f"状态: {model.status}")
        
        print("\n=== 修改后的API密钥信息 ===")
        print(f"ID: {api_key.id}")
        print(f"名称: {api_key.name}")
        print(f"平台: {api_key.platform}")
        print(f"状态: {api_key.status}")
        print(f"URL: {api_key.url}")
        
        print("\n⚠️  请确保在 ai_api_key 表中填入正确的智谱AI API密钥")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 切换失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    switch_to_zhipu()
