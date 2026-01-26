import sys
from pathlib import Path

# 添加脚本路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "scripts"))

from persistence import save_game, LATEST_SAVE, SAVES_DIR

def check_sync():
    print(f"LATEST_SAVE path: {LATEST_SAVE.absolute()}")
    test_data = {"test": "sync_check", "val": 123}
    
    # 获取当前 LATEST_SAVE 的状态
    old_content = LATEST_SAVE.read_text(encoding="utf-8") if LATEST_SAVE.exists() else None
    
    # 执行保存
    path = save_game(test_data)
    print(f"Saved backup to: {path}")
    
    # 检查 LATEST_SAVE 是否更新
    new_content = LATEST_SAVE.read_text(encoding="utf-8")
    
    if old_content == new_content:
        print("FAILED: latest_save.json was NOT updated!")
    else:
        print("SUCCESS: latest_save.json was updated.")
        
    # 列出目录
    print("\nFiles in saves dir:")
    for f in SAVES_DIR.glob("*.json"):
        print(f"- {f.name} ({f.stat().st_size} bytes)")

if __name__ == "__main__":
    check_sync()
