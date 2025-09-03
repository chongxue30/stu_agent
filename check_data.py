from app.db.session import SessionLocal
from sqlalchemy import text

def check_data():
    db = SessionLocal()
    try:
        # 检查会话数据
        conversation = db.execute(text(
            "SELECT * FROM ai_chat_conversation WHERE id = :id"
        ), {"id": "1781604279872581774"}).fetchone()
        
        if conversation:
            print("\n=== 会话信息 ===")
            print(f"ID: {conversation.id}")
            print(f"模型ID: {conversation.model_id}")
            print(f"模型标识: {conversation.model}")
            print(f"角色ID: {conversation.role_id}")
            
            # 检查关联的模型
            if conversation.model_id:
                model = db.execute(text(
                    "SELECT * FROM ai_model WHERE id = :id"
                ), {"id": conversation.model_id}).fetchone()
                
                if model:
                    print("\n=== 模型信息 ===")
                    print(f"ID: {model.id}")
                    print(f"名称: {model.name}")
                    print(f"标识: {model.model}")
                    print(f"平台: {model.platform}")
                    print(f"状态: {model.status}")
                    print(f"API密钥ID: {model.key_id}")
                    
                    # 检查关联的API密钥
                    if model.key_id:
                        api_key = db.execute(text(
                            "SELECT * FROM ai_api_key WHERE id = :id"
                        ), {"id": model.key_id}).fetchone()
                        
                        if api_key:
                            print("\n=== API密钥信息 ===")
                            print(f"ID: {api_key.id}")
                            print(f"名称: {api_key.name}")
                            print(f"平台: {api_key.platform}")
                            print(f"状态: {api_key.status}")
                            print(f"URL: {api_key.url}")
                        else:
                            print("\n❌ API密钥不存在")
                    else:
                        print("\n❌ 模型未关联API密钥")
                else:
                    print("\n❌ 模型不存在")
            else:
                print("\n❌ 会话未关联模型")
        else:
            print("\n❌ 会话不存在")
            
        # 列出所有可用的模型
        print("\n=== 所有可用模型 ===")
        models = db.execute(text(
            "SELECT * FROM ai_model WHERE deleted = 0 AND status = 0"
        )).fetchall()
        
        for m in models:
            print(f"ID: {m.id}, 名称: {m.name}, 平台: {m.platform}, 状态: {m.status}")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_data()