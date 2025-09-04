from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model

def restore_all_models():
    db: Session = SessionLocal()
    try:
        models = db.query(Model).all()
        for model_obj in models:
            if model_obj.deleted:
                model_obj.deleted = 0
                db.add(model_obj)
                print(f"模型 ID {model_obj.id} ({model_obj.name}) 已恢复。")
        db.commit()
        print("所有已删除的模型已恢复。")
    except Exception as e:
        db.rollback()
        print(f"恢复失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    restore_all_models()
