import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

# 获取技能根目录
SKILL_ROOT = Path(__file__).parent.parent
SAVES_DIR = SKILL_ROOT / "assets" / "saves"
DB_PATH = SAVES_DIR / "wuxiaX.db"

def ensure_db():
    if not DB_PATH.exists():
        from db_init import init_db
        init_db()

def save_game(data, chapter="未知", location="未知"):
    """
    保存游戏数据到 SQLite 数据库
    """
    ensure_db()
    
    timestamp = datetime.now().isoformat()
    # 提取元数据
    metadata = {
        "version": "2.0.0",
        "save_type": "sqlite"
    }
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO game_saves (timestamp, chapter, location, data_json, metadata_json)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, chapter, location, json.dumps(data, ensure_ascii=False), json.dumps(metadata)))
    
    save_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return f"DB_SAVE_ID_{save_id}"

def load_game(save_id=None):
    """
    读取存档数据。如果 save_id 为空，读取最新存档。
    """
    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if save_id:
        cursor.execute("SELECT data_json FROM game_saves WHERE id = ?", (save_id,))
    else:
        cursor.execute("SELECT data_json FROM game_saves ORDER BY id DESC LIMIT 1")
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return None

if __name__ == "__main__":
    # 示例测试
    test_data = {"test": "sqlite_data"}
    save_info = save_game(test_data, "测试章节", "大研镇")
    print(f"存档已保存：{save_info}")
    loaded = load_game()
    print(f"读取数据成功: {loaded == test_data}")
