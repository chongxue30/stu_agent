from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.ai.model import Model

def get_all_models():
    db: Session = SessionLocal()
    try:
        models = db.query(Model).all()
        for m in models:
            print(f"ID: {m.id}, Name: {m.name}, Platform: {m.platform}, Model: {m.model}, Key ID: {m.key_id}, Sort: {m.sort}, Status: {m.status}, Creator: {m.creator}, Create Time: {m.create_time}, Updater: {m.updater}, Update Time: {m.update_time}, Deleted: {m.deleted}, User ID: {m.user_id}, Tenant ID: {m.tenant_id}")
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    get_all_models()
