import sqlite3
import json
from pathlib import Path
from datetime import datetime

class GameMemory:
    """
    武侠世界记忆中枢：负责长期记忆（数据库）与短期记忆（内存/缓存）的存取。
    """
    def __init__(self, db_path=None):
        if db_path is None:
            # 默认存储在技能的 assets 目录下
            self.db_path = Path(__file__).parent.parent / "assets" / "game_memory.db"
        else:
            self.db_path = Path(db_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self.short_term = [] # 短期记忆缓存

    def _init_db(self):
        """初始化长期记忆表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 长期记忆：存储关键事件、人物好感度重大转折、世界线变动
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS long_term_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    key_event TEXT,
                    details TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 实体状态快照
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entity_snapshots (
                    entity_name TEXT PRIMARY KEY,
                    state_data TEXT,
                    last_update DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_long_term(self, category, event, details=""):
        """铭刻一段长久记忆"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO long_term_memory (category, key_event, details) VALUES (?, ?, ?)",
                (category, event, details)
            )
            conn.commit()

    def query_long_term(self, category=None):
        """回溯长久记忆"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT * FROM long_term_memory WHERE category = ? ORDER BY timestamp DESC", (category,))
            else:
                cursor.execute("SELECT * FROM long_term_memory ORDER BY timestamp DESC")
            return cursor.fetchall()

    def save_entity_state(self, name, data):
        """记录实体（如NPC、物品）的最新神识快照"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO entity_snapshots (entity_name, state_data, last_update) VALUES (?, ?, ?)",
                (name, json.dumps(data, ensure_ascii=False), datetime.now().isoformat())
            )
            conn.commit()

    def add_short_term(self, narrative):
        """暂存短期记忆（如当前章节的即时描写）"""
        self.short_term.append({
            "narrative": narrative,
            "timestamp": datetime.now().isoformat()
        })
        # 仅保留最近 10 条
        if len(self.short_term) > 10:
            self.short_term.pop(0)

if __name__ == "__main__":
    memory = GameMemory()
    memory.add_long_term("江湖秘闻", "江未央击败了圣堂守卫", "守卫临终前交出了一枚染血的玉佩")
    print("记忆已铭刻。")
