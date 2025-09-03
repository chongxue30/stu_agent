from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model

def update_deepseek_model_name():
    db: Session = SessionLocal()
    try:
        model_obj = db.query(Model).filter(Model.id == 57).first()
        if model_obj:
            model_obj.model = "deepseek-chat"
            db.add(model_obj)
            db.commit()
            db.refresh(model_obj)
            print(f"模型 ID 57 的名称已更新为: {model_obj.model}")
        else:
            print("未找到 ID 为 57 的模型")
    except Exception as e:
        db.rollback()
        print(f"更新失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_deepseek_model_name()
