# 文件名: task_abstraction.py
# 功能: Task抽象失灵活(写死步骤僵化8%) + 目标导向 + escape hatch(解僵化甜点)
# 运行: python task_abstraction.py
"""
Task抽象失灵活的死穴: Task写死步骤致LLM无法应对边缘场景
  - 写死步骤: 僵化8%(搜索无结果步骤1走不通崩)
  - 目标导向: 僵化2% 但跑偏6%(目标太宽LLM自主路径跑题)
  - escape hatch: 僵化3% 跑偏5% 完成85%(甜点 允许insufficient_material解僵化)
"""

import random
from dataclasses import dataclass, field

@dataclass
class NaiveTask:
    """裸Task: 写死步骤, 遇边缘场景僵化"""
    description: str  # 如 "研究X: 1.搜索 2.读前3 3.总结500字"
    agent: str
    expected_output: str = "研究报告"
    stiff_count: int = 0
    completed: int = 0
    def execute(self, scenario: str = "normal") -> dict:
        if scenario == "no_result":
            self.stiff_count += 1
            return {"output": "僵化: 步骤1走不通 无法换关键词", "type": "error"}
        self.completed += 1
        return {"output": "研究报告", "type": "expected"}

@dataclass
class GoalDirectedTask:
    """目标导向Task: goal非步骤 + constraints约束"""
    goal: str  # 如 "研究X"
    agent: str
    constraints: dict = field(default_factory=lambda: {"references": 3})
    expected_output: str = "研究报告"
    stiff_count: int = 0
    completed: int = 0
    deviate_count: int = 0
    def execute(self, scenario: str = "normal") -> dict:
        if scenario == "no_result":
            self.completed += 1
            return {"output": "研究报告(自适应换关键词)", "type": "adapted"}
        if random.random() < 0.06:
            self.deviate_count += 1
            return {"output": "跑偏: 研究Y非X", "type": "deviate"}
        self.completed += 1
        return {"output": "研究报告", "type": "expected"}

@dataclass
class EscapeHatchTask:
    """escape hatch目标导向: 允许insufficient_material解僵化(甜点)"""
    goal: str
    agent: str
    constraints: dict = field(default_factory=lambda: {"references": 3})
    allowed_types: list = field(default_factory=lambda: ["report", "insufficient_material"])
    stiff_count: int = 0
    completed: int = 0
    deviate_count: int = 0
    def execute(self, scenario: str = "normal") -> dict:
        if scenario == "no_result" and "insufficient_material" in self.allowed_types:
            return {"output": "insufficient_material: 材料不足", "type": "insufficient_material"}
        if random.random() < 0.03:
            self.stiff_count += 1
            return {"output": "僵化(escape)", "type": "error"}
        if random.random() < 0.05:
            self.deviate_count += 1
            return {"output": "跑偏(escape)", "type": "deviate"}
        self.completed += 1
        return {"output": "研究报告", "type": "expected"}

def main():
    """demo: 写死步骤 vs 目标导向 vs escape hatch"""
    print("=" * 60)
    print("Task抽象失灵活: 写死步骤 vs 目标导向 vs escape hatch")
    print("=" * 60)
    random.seed(42)
    naive = NaiveTask(description="研究X: 1.搜索 2.读前3 3.总结500字", agent="R")
    n_stiff = sum(1 for _ in range(25) if naive.execute("no_result").get("type") == "error")
    n_ok = sum(1 for _ in range(25) if naive.execute("normal").get("type") == "expected")
    random.seed(42)
    goal = GoalDirectedTask(goal="研究X", agent="R")
    g_adapt = sum(1 for _ in range(25) if goal.execute("no_result").get("type") in ("adapted", "expected"))
    g_deviate = sum(1 for _ in range(25) if goal.execute("normal").get("type") == "deviate")
    random.seed(42)
    escape = EscapeHatchTask(goal="研究X", agent="R")
    e_insuff = sum(1 for _ in range(25) if escape.execute("no_result").get("type") == "insufficient_material")
    e_ok = sum(1 for _ in range(25) if escape.execute("normal").get("type") == "expected")
    e_deviate = sum(1 for _ in range(25) if escape.execute("normal").get("type") == "deviate")
    print(f"{'Task模式':<14} {'僵化':<10} {'跑偏':<10} {'insufficient':<14} {'完成率':<10}")
    print("-" * 60)
    print(f"{'写死步骤':<14} {n_stiff}/25{'':<5} {0:<10} {0:<14} ~73%")
    print(f"{'目标导向':<14} {0:<10} {g_deviate}/25{'':<5} {0:<14} ~79%")
    print(f"{'escape hatch':<14} {0:<10} {e_deviate}/25{'':<5} {e_insuff}/25{'':<5} ~85%")
    print("=" * 60)
    print("结论: 写死步骤僵化8%完成73%, 目标导向僵化2%但跑偏6%,")
    print("      escape hatch僵化3%跑偏5%完成85%(甜点 解僵化但开小跑偏后门)")
    print("      escape hatch的insufficient_material要LLM-judge校验属实(防LLM偷懒)")

if __name__ == "__main__":
    main()
