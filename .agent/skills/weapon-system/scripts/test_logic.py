import random

class Weapon:
    def __init__(self, name, max_durability, quality="Common"):
        self.name = name
        self.max_durability = max_durability
        self.durability = max_durability
        self.quality = quality
        self.broken = False

    def consume(self, amount):
        if self.quality == "Divine":
            amount = amount * 0.5  # 神兵损耗减半
        
        self.durability -= amount
        if self.durability <= 0:
            self.durability = 0
            self.broken = True
        return self.durability

    def get_power_multiplier(self):
        ratio = self.durability / self.max_durability
        if ratio > 0.5:
            return 1.0
        elif ratio > 0.2:
            return 0.8
        else:
            return 0.5

def test_weapon_system():
    # 测试 1: 普通武器损耗
    sword = Weapon("铁剑", 100)
    sword.consume(60)
    print(f"[{sword.name}] 耐久剩余: {sword.durability}, 威力倍率: {sword.get_power_multiplier()}")
    assert sword.get_power_multiplier() == 0.8
    
    # 测试 2: 神兵特权
    god_blade = Weapon("屠龙刀", 100, quality="Divine")
    god_blade.consume(60)
    print(f"[{god_blade.name}] 耐久剩余: {god_blade.durability}, 威力倍率: {god_blade.get_power_multiplier()}")
    assert god_blade.durability == 70.0 # 60 * 0.5 = 30 consumed
    
    # 测试 3: 损坏判定
    rust_knife = Weapon("锈刀", 10)
    rust_knife.consume(15)
    print(f"[{rust_knife.name}] 是否损毁: {rust_knife.broken}")
    assert rust_knife.broken == True

if __name__ == "__main__":
    test_weapon_system()
    print("\n<test_success>武器系统核心逻辑验证通过!</test_success>")
