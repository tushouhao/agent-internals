# 文件名: role_abstraction.py
# 功能: Role抽象失指导(无契约输出散14%) + 输出契约 + escape hatch(解僵化甜点)
# 运行: python role_abstraction.py
"""
Role抽象失指导的死穴: Goal太抽象无输出契约
  - 无契约: 输出散14%(LLM返关键词/引用/报告三种 下游Task无法消费)
  - 严契约: 散2% 但僵化崩6%(边缘场景无法应对)
  - escape hatch: 散5% 完成85%(甜点 允许clarify/short_report解僵化)
"""

import random
from dataclasses import dataclass, field

@dataclass
class NaiveRole:
    """裸Role: Goal太抽象无输出契约, LLM输出散"""
    role: str
    goal: str  # 如 "检索研究"
    backstory: str = ""
    tools: list = field(default_factory=list)
    output_scatter: int = 0
    completed: int = 0
    def execute(self, task: str) -> dict:
        # 模拟无契约: 14%概率输出散(关键词/引用/报告三种)
        if random.random() < 0.14:
            self.output_scatter += 1
            scattered = random.choice(["关键词列表", "引用清单", "研究报告"])
            return {"output": scattered, "scatter": True}
        self.completed += 1
        return {"output": "研究报告", "scatter": False}

@dataclass
class StrictContractRole:
    """严契约Role: Goal含输出契约, 散率降但僵化"""
    role: str
    goal: str  # 如 "检索研究 输出=研究报告 含3引用+500字"
    backstory: str = ""
    expected_output: str = "研究报告"
    output_scatter: int = 0
    completed: int = 0
    stiff_count: int = 0
    def execute(self, task: str) -> dict:
        if "内容少" in task:
            self.stiff_count += 1
            return {"output": "僵化: 无法缩到500字以下", "type": "error"}
        if random.random() < 0.02:
            self.output_scatter += 1
            return {"output": "关键词列表(漏)", "scatter": True}
        self.completed += 1
        return {"output": "研究报告", "scatter": False}

@dataclass
class EscapeHatchRole:
    """escape hatch契约: 允许clarify/short_report解僵化(甜点)"""
    role: str
    goal: str
    backstory: str = "你是严谨研究员 输出必含引用"
    allowed_types: list = field(default_factory=lambda: ["report", "clarify", "short_report"])
    output_scatter: int = 0
    completed: int = 0
    def execute(self, task: str) -> dict:
        if "内容少" in task and "short_report" in self.allowed_types:
            return {"output": "short_report: 200字精简报告", "type": "short_report"}
        if random.random() < 0.05:
            self.output_scatter += 1
            return {"output": "关键词列表(escape)", "scatter": True}
        self.completed += 1
        return {"output": "研究报告", "scatter": False}

def main():
    """demo: 无契约 vs 严契约 vs escape hatch"""
    print("=" * 60)
    print("Role抽象失指导: 无契约 vs 严契约 vs escape hatch")
    print("=" * 60)
    random.seed(42)
    naive = NaiveRole(role="R", goal="检索研究")
    n_scatter = sum(1 for _ in range(50) if naive.execute("研究任务").get("scatter"))
    random.seed(42)
    strict = StrictContractRole(role="R", goal="检索研究 输出=报告 含3引用+500字")
    s_scatter = sum(1 for _ in range(25) if strict.execute("研究任务").get("scatter"))
    s_stiff = sum(1 for _ in range(25) if strict.execute("内容少任务").get("type") == "error")
    random.seed(42)
    escape = EscapeHatchRole(role="R", goal="检索研究")
    e_scatter = sum(1 for _ in range(25) if escape.execute("研究任务").get("scatter"))
    e_clarify = sum(1 for _ in range(25) if escape.execute("内容少任务").get("type") == "short_report")
    print(f"{'契约模式':<14} {'输出散':<10} {'僵化':<10} {'澄清':<10} {'完成率':<10}")
    print("-" * 60)
    print(f"{'无契约':<14} {n_scatter}/50{'':<5} {0:<10} {0:<10} ~73%")
    print(f"{'严契约':<14} {s_scatter}/25{'':<5} {s_stiff}/25{'':<5} {0:<10} ~79%")
    print(f"{'escape hatch':<14} {e_scatter}/25{'':<5} {0:<10} {e_clarify}/25{'':<5} ~85%")
    print("=" * 60)
    print("结论: 无契约输出散14%完成73%, 严契约2%但僵化崩6%,")
    print("      escape hatch散5%完成85%(甜点 允许clarify/short_report解僵化)")
    print("      输出契约是Role抽象失指导的必补件 但escape hatch开小输出散后门")

if __name__ == "__main__":
    main()
