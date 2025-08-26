#!/usr/bin/env python3
"""
初始化字典数据脚本
"""
from app.db.session import SessionLocal
from app.models.system.dict_type import DictType
from app.models.system.dict_data import DictData
from sqlalchemy.sql import func

def init_dict_data():
    """初始化字典数据"""
    db = SessionLocal()
    try:
        print("🗂️ 开始初始化字典数据...")
        
        # 1. 创建字典类型
        dict_types = [
            {
                "name": "系统状态",
                "type": "sys_status",
                "status": 0,
                "remark": "系统状态字典"
            },
            {
                "name": "用户性别",
                "type": "sys_user_sex",
                "status": 0,
                "remark": "用户性别字典"
            },
            {
                "name": "平台类型",
                "type": "ai_platform",
                "status": 0,
                "remark": "AI平台类型字典"
            }
        ]
        
        for type_data in dict_types:
            existing = db.query(DictType).filter(DictType.type == type_data["type"]).first()
            if not existing:
                dict_type = DictType(**type_data)
                db.add(dict_type)
                print(f"✅ 创建字典类型: {type_data['name']}")
            else:
                print(f"⏭️ 字典类型已存在: {type_data['name']}")
        
        db.commit()
        
        # 2. 创建字典数据
        dict_data_list = [
            # 系统状态
            {
                "sort": 1,
                "label": "正常",
                "value": "0",
                "dict_type": "sys_status",
                "status": 0,
                "color_type": "success",
                "css_class": "btn-success"
            },
            {
                "sort": 2,
                "label": "停用",
                "value": "1",
                "dict_type": "sys_status",
                "status": 0,
                "color_type": "danger",
                "css_class": "btn-danger"
            },
            # 用户性别
            {
                "sort": 1,
                "label": "男",
                "value": "1",
                "dict_type": "sys_user_sex",
                "status": 0,
                "color_type": "primary",
                "css_class": "btn-primary"
            },
            {
                "sort": 2,
                "label": "女",
                "value": "2",
                "dict_type": "sys_user_sex",
                "status": 0,
                "color_type": "info",
                "css_class": "btn-info"
            },
            # AI平台类型
            {
                "sort": 1,
                "label": "OpenAI",
                "value": "openai",
                "dict_type": "ai_platform",
                "status": 0,
                "color_type": "primary",
                "css_class": "btn-primary"
            },
            {
                "sort": 2,
                "label": "智谱AI",
                "value": "zhipu",
                "dict_type": "ai_platform",
                "status": 0,
                "color_type": "success",
                "css_class": "btn-success"
            },
            {
                "sort": 3,
                "label": "DeepSeek",
                "value": "deepseek",
                "dict_type": "ai_platform",
                "status": 0,
                "color_type": "warning",
                "css_class": "btn-warning"
            }
        ]
        
        for data in dict_data_list:
            existing = db.query(DictData).filter(
                DictData.dict_type == data["dict_type"],
                DictData.value == data["value"]
            ).first()
            
            if not existing:
                dict_data = DictData(**data)
                db.add(dict_data)
                print(f"✅ 创建字典数据: {data['label']} ({data['dict_type']})")
            else:
                print(f"⏭️ 字典数据已存在: {data['label']} ({data['dict_type']})")
        
        db.commit()
        print("🎉 字典数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_dict_data()
