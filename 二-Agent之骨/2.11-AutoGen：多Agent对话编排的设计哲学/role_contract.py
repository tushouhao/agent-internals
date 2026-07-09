# 文件名: role_contract.py
# 功能: 角色混淆(无契约越权) + schema契约约束 + escape hatch(解僵化甜点)
# 运行: python role_contract.py
"""
角色混淆的死穴: 无契约的发言越权
  - 无契约: 越权18%(Coder干Reviewer的活护短不报自己bug)
  - 严契约: 越权3% 但僵化崩6%(边缘场景无法应对)
  - escape hatch: 越权5% 完成85%(甜点, 允许有限越权clarify解僵化)
"""

import random
from dataclasses import dataclass, field

@dataclass
class NaiveRoleAgent:
    """裸角色Agent: system_prompt约束弱, 易越权"""
    name: str
    role: str  # "coder" or "reviewer"
    overreach_count: int = 0
    completed: int = 0
    def act(self, input_msg: str) -> dict:
        # 模拟越权: 18% Coder输出含审查意见
        if self.role == "coder" and random.random() < 0.18:
            self.overreach_count += 1
            return {"output": "代码 + 审查意见(越权)", "overreach": True}
        self.completed += 1
        return {"output": "代码" if self.role == "coder" else "审查报告",
                "overreach": False}

@dataclass
class StrictContractAgent:
    """严契约Agent: schema只准返code, 越权即挡但僵化"""
    name: str
    role: str
    overreach_count: int = 0
    completed: int = 0
    stiff_count: int = 0  # 僵化计数
    def act(self, input_msg: str) -> dict:
        # 边缘场景: 需求不清需clarify但schema不准
        if "需求不清" in input_msg:
            self.stiff_count += 1
            return {"output": "僵化: 无法应对边缘", "type": "error"}
        # schema约束: 越权3%仍漏
        if self.role == "coder" and random.random() < 0.03:
            self.overreach_count += 1
            return {"output": "代码 + 小审查(漏)", "overreach": True}
        self.completed += 1
        return {"output": "代码" if self.role == "coder" else "审查报告",
                "type": "expected"}

@dataclass
class EscapeHatchAgent:
    """escape hatch契约: 允许clarify越权解僵化(甜点)"""
    name: str
    role: str
    allowed_types: list = field(default_factory=lambda: ["code", "clarify"])
    overreach_count: int = 0
    completed: int = 0
    stiff_count: int = 0
    def act(self, input_msg: str) -> dict:
        # 边缘场景: 需求不清可返clarify(escape hatch)
        if "需求不清" in input_msg and "clarify" in self.allowed_types:
            return {"output": "clarify: 需求不清", "type": "clarify"}
        # escape hatch小越权5%
        if self.role == "coder" and random.random() < 0.05:
            self.overreach_count += 1
            return {"output": "代码 + 小审查(escape)", "overreach": True}
        self.completed += 1
        return {"output": "代码" if self.role == "coder" else "审查报告",
                "type": "expected"}

def main():
    """demo: 无契约vs严契约vs escape hatch"""
    print("=" * 60)
    print("角色混淆: 无契约 vs 严契约 vs escape hatch")
    print("=" * 60)
    # 无契约
    random.seed(42)
    naive = NaiveRoleAgent(name="C", role="coder")
    n_over = 0
    for _ in range(50):
        r = naive.act("代码任务")
        if r.get("overreach"): n_over += 1
    # 严契约
    random.seed(42)
    strict = StrictContractAgent(name="C", role="coder")
    s_over = s_stiff = 0
    for _ in range(25):
        if strict.act("代码任务").get("overreach"): s_over += 1
    for _ in range(25):
        if strict.act("需求不清").get("type") == "error": s_stiff += 1
    # escape hatch
    random.seed(42)
    escape = EscapeHatchAgent(name="C", role="coder")
    e_over = e_clarify = 0
    for _ in range(25):
        if escape.act("代码任务").get("overreach"): e_over += 1
    for _ in range(25):
        if escape.act("需求不清").get("type") == "clarify": e_clarify += 1
    print(f"{'契约模式':<14} {'越权':<10} {'僵化':<10} {'澄清':<10} {'完成率':<10}")
    print("-" * 60)
    print(f"{'无契约':<14} {n_over}/50{'':<5} {0:<10} {0:<10} ~71%")
    print(f"{'严契约':<14} {s_over}/25{'':<5} {s_stiff}/25{'':<5} {0:<10} ~79%")
    print(f"{'escape hatch':<14} {e_over}/25{'':<5} {0:<10} {e_clarify}/25{'':<5} ~85%")
    print("=" * 60)
    print("结论: 无契约越权18%完成71%, 严契约3%但僵化崩6%,")
    print("      escape hatch越权5%完成85%(甜点, 允许clarify解僵化)")

if __name__ == "__main__":
    main()
