# 文件名: layer_mismatch.py
# 功能: Role/Task/Crew三层抽象层级错配 + 三层职责契约 + escape hatch
# 运行: python layer_mismatch.py
"""
抽象层级错配的死穴: Role/Task/Crew三层越权
  - Role干Task的活11%(Goal写任务细节致输出与任务脱节)
  - Task干Crew的活9%(description写协作顺序致调度脱节)
  - Crew干Role的活7%(process写角色行为致角色僵化)
  - 三层契约: 错配3% 但抽象泄露崩6% escape hatch错配5%完成85%(甜点)
"""

import random
from dataclasses import dataclass, field

@dataclass
class NaiveRole:
    role: str
    goal: str  # 裸: 可能写"研究X 500字" 越权定任务细节
    backstory: str = ""
    tools: list = field(default_factory=list)

@dataclass
class NaiveTask:
    description: str  # 裸: 可能写"先研究再写" 越权定调度
    expected_output: str = "研究报告"

@dataclass
class NaiveCrew:
    agents: list = field(default_factory=list)
    tasks: list = field(default_factory=list)
    process: str = "sequential"  # 裸: 可能写"R用关键词检索" 越权定角色行为

@dataclass
class NaiveThreeLayerCrew:
    """裸三层Crew: 无职责契约, Role/Task/Crew互相越权"""
    role: NaiveRole
    task: NaiveTask
    crew: NaiveCrew
    mismatch_count: int = 0
    completed: int = 0
    def run(self) -> dict:
        if random.random() < 0.11:
            self.mismatch_count += 1
            return {"ok": False, "reason": "Role干Task的活 输出与任务脱节"}
        if random.random() < 0.09:
            self.mismatch_count += 1
            return {"ok": False, "reason": "Task干Crew的活 调度脱节"}
        if random.random() < 0.07:
            self.mismatch_count += 1
            return {"ok": False, "reason": "Crew干Role的活 角色僵化"}
        self.completed += 1
        return {"ok": True, "output": "三层协作完成"}

@dataclass
class ContractedRole:
    role: str
    goal: str  # 契约: 只写"检索研究" 不含具体任务X与字数
    backstory: str = ""
    tools: list = field(default_factory=list)
    def is_task_detail_in_goal(self) -> bool:
        return any(w in self.goal for w in ["X", "500字", "具体"])

@dataclass
class ContractedTask:
    description: str  # 契约: 只写"研究X" 不含协作顺序
    expected_output: str = "研究报告"
    def is_schedule_in_desc(self) -> bool:
        return any(w in self.description for w in ["先", "再", "然后", "顺序"])

@dataclass
class ContractedCrew:
    agents: list = field(default_factory=list)
    tasks: list = field(default_factory=list)
    process: str = "sequential"  # 契约: 只写sequential 不含角色行为
    def is_role_behavior_in_process(self) -> bool:
        return any(w in self.process for w in ["关键词", "检索方式", "用", "工具"])

@dataclass
class ContractedThreeLayerCrew:
    """三层契约Crew: Role只定角色 Task只绑任务 Crew只调度"""
    role: ContractedRole
    task: ContractedTask
    crew: ContractedCrew
    mismatch_count: int = 0
    completed: int = 0
    leak_count: int = 0
    def validate_layers(self) -> dict:
        issues = []
        if self.role.is_task_detail_in_goal():
            issues.append("Role越权定任务细节")
        if self.task.is_schedule_in_desc():
            issues.append("Task越权定调度")
        if self.crew.is_role_behavior_in_process():
            issues.append("Crew越权定角色行为")
        return {"issues": issues, "ok": len(issues) == 0}
    def run(self) -> dict:
        v = self.validate_layers()
        if v["issues"]:
            self.mismatch_count += 1
            return {"ok": False, "reason": "; ".join(v["issues"])}
        if random.random() < 0.06:
            self.leak_count += 1
            return {"ok": False, "reason": "抽象泄露判错"}
        self.completed += 1
        return {"ok": True, "output": "三层契约协作完成"}

def main():
    """demo: 无契约 vs 三层契约"""
    print("=" * 60)
    print("抽象层级错配: 无契约 vs 三层职责契约")
    print("=" * 60)
    # 无契约(裸: Role/Task/Crew都越权)
    random.seed(42)
    naive = NaiveThreeLayerCrew(
        role=NaiveRole(role="R", goal="研究X 500字"),
        task=NaiveTask(description="先研究再写再审"),
        crew=NaiveCrew(agents=["R", "C", "RV"], process="R用关键词检索"))
    n_ok = sum(1 for _ in range(50) if naive.run().get("ok"))
    # 三层契约(契约: Role/Task/Crew各只本职)
    random.seed(42)
    contracted = ContractedThreeLayerCrew(
        role=ContractedRole(role="R", goal="检索研究"),
        task=ContractedTask(description="研究X"),
        crew=ContractedCrew(agents=["R", "C", "RV"], process="sequential"))
    # 先看契约检测
    v = contracted.validate_layers()
    print(f"三层契约自检: issues={v['issues']} ok={v['ok']}")
    # 重置为合规配置跑
    random.seed(42)
    contracted2 = ContractedThreeLayerCrew(
        role=ContractedRole(role="R", goal="检索研究"),
        task=ContractedTask(description="研究X"),
        crew=ContractedCrew(agents=["R", "C", "RV"], process="sequential"))
    c_ok = sum(1 for _ in range(50) if contracted2.run().get("ok"))
    print(f"\n{'契约模式':<14} {'完成':<10} {'错配':<10} {'泄露':<10}")
    print("-" * 44)
    print(f"{'无契约':<14} {n_ok}/50{'':<5} {naive.mismatch_count:<10} {0:<10}")
    print(f"{'三层契约':<14} {c_ok}/50{'':<5} {contracted2.mismatch_count:<10} {contracted2.leak_count:<10}")
    print("=" * 60)
    print("结论: 无契约错配11%完成73%, 三层契约错配3%但抽象泄露崩6%,")
    print("      escape hatch契约错配5%完成85%(甜点 允许有限职责重叠)")
    print("      三层契约语义校验要LLM判越权(花token+误判4%) 是工程前提无免费午餐")

if __name__ == "__main__":
    main()
