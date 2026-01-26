import sys
import json
from pathlib import Path
import time

# 添加路径
scripts_dir = Path("./scripts")
sys.path.append(str(scripts_dir))

from persistence import save_game, LATEST_SAVE

def verify_atomic_sync():
    print("--- 验证存档同步逻辑 ---")
    
    unique_val = f"verify_{int(time.time())}"
    test_data = {
        "protagonist": {"name": "江未央", "test_val": unique_val},
        "world": {"status": "testing"}
    }
    
    print(f"正在执行存档，特征值: {unique_val}")
    backup_path = save_game(test_data)
    
    # 1. 检查备份文件是否存在
    backup_file = Path(backup_path)
    if not backup_file.exists():
        print("错误: 备份文件未创建")
        return False
    
    # 2. 检查 latest_save.json 是否存在
    if not LATEST_SAVE.exists():
        print("错误: latest_save.json 不存在")
        return False
        
    # 3. 比较内容
    with open(backup_file, "r", encoding="utf-8") as f1, open(LATEST_SAVE, "r", encoding="utf-8") as f2:
        c1 = json.load(f1)
        c2 = json.load(f2)
        
    if c1 == c2 and c1["protagonist"]["test_val"] == unique_val:
        print("成功: latest_save.json 与备份文件内容一致且特征值匹配！")
        return True
    else:
        print("失败: latest_save.json 与备份文件不一致")
        return False

if __name__ == "__main__":
    verify_atomic_sync()
