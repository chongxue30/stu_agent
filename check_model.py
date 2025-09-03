from app.db.session import SessionLocal
from sqlalchemy import text

def check_and_fix_model():
    db = SessionLocal()
    try:
        # 检查模型状态
        model = db.execute(text("""
            SELECT * FROM ai_model WHERE id = 57
        """)).fetchone()
        
        print("\n=== 当前模型状态 ===")
        print(f"ID: {model.id}")
        print(f"名称: {model.name}")
        print(f"标识: {model.model}")
        print(f"平台: {model.platform}")
        print(f"状态: {model.status}")
        print(f"已删除: {model.deleted}")
        
        # 恢复模型（取消删除标记）
        db.execute(text("""
            UPDATE ai_model 
            SET deleted = 0 
            WHERE id = 57
        """))
        
        db.commit()
        print("\n✅ 已恢复模型")
        
        # 验证修改
        model = db.execute(text("""
            SELECT * FROM ai_model WHERE id = 57
        """)).fetchone()
        
        print("\n=== 修改后的状态 ===")
        print(f"ID: {model.id}")
        print(f"名称: {model.name}")
        print(f"标识: {model.model}")
        print(f"平台: {model.platform}")
        print(f"状态: {model.status}")
        print(f"已删除: {model.deleted}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 操作失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_and_fix_model()
