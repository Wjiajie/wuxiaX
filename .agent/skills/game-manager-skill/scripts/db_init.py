import sqlite3
from pathlib import Path

# 获取技能根目录
SKILL_ROOT = Path(__file__).parent.parent
SAVES_DIR = SKILL_ROOT / "assets" / "saves"
DB_PATH = SAVES_DIR / "wuxiaX.db"

def init_db():
    if not SAVES_DIR.exists():
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建存档表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_saves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            chapter TEXT,
            location TEXT,
            data_json TEXT NOT NULL,
            metadata_json TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"数据库初始化成功：{DB_PATH}")

if __name__ == "__main__":
    init_db()
