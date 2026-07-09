# 文件名: crew_boundary.py
# 功能: 角色化协作失效边界三红线判据 + 三类任务完成率基线
# 运行: python crew_boundary.py
"""
角色化协作失效边界三红线:
  - Role红线: Goal抽象率 ≥ 30% 输出散超14%
  - Task红线: 任务开放率 ≥ 25% 僵化超8%
  - Crew红线: 并行任务率 ≥ 20% 协作僵化超22%
  判决: 0红线裸Crew够用, 1手补, 2弃Crew转编排
"""

from dataclasses import dataclass

@dataclass
class CrewSuitabilityChecker:
    """角色化协作适用性判据: 三红线"""
    goal_abstract_ratio: float  # Goal抽象率
    task_open_ratio: float  # 任务开放率
    parallel_ratio: float  # 并行任务率
    def verdict(self) -> dict:
        if (self.goal_abstract_ratio < 0.30 and
            self.task_open_ratio < 0.25 and
            self.parallel_ratio < 0.20):
            return {"verdict": "裸Crew够用", "替代": "CrewAI裸Crew",
                    "完成率预期": "73%多角色甜点"}
        if (0.30 <= self.goal_abstract_ratio < 0.50 or
            self.parallel_ratio >= 0.20):
            return {"verdict": "用混合谱系", "替代": "CrewAI+LangGraph混合",
                    "完成率预期": "88%"}
        risks = []
        if self.goal_abstract_ratio >= 0.50:
            risks.append({"redline": "Role抽象失指导", "fix": "加输出契约或转编排"})
        if self.task_open_ratio >= 0.25:
            risks.append({"redline": "Task抽象失灵活", "fix": "改目标导向或转编排"})
        if self.parallel_ratio >= 0.40:
            risks.append({"redline": "Crew协作僵化", "fix": "升Flow或转编排"})
        if len(risks) >= 2:
            return {"verdict": "弃Crew转编排", "risks": risks,
                    "替代": "LangGraph编排或自研(2.15)", "完成率预期": "85-89%"}
        return {"verdict": "手补Crew可用", "risks": risks,
                "替代": "契约+目标导向+Flow", "完成率预期": "85%"}

@dataclass
class TaskCompletionBaseline:
    """三类任务完成率基线"""
    task_type: str
    naive_crew: float
    patched_crew: float
    hybrid_spectrum: float
    full_harness: float
    def summary(self) -> dict:
        return {"task_type": self.task_type,
                "裸Crew": f"{self.naive_crew:.0%}",
                "手补Crew": f"{self.patched_crew:.0%}",
                "混合谱系": f"{self.hybrid_spectrum:.0%}",
                "完整harness": f"{self.full_harness:.0%}"}

def main():
    """demo: 三红线判据 + 三类任务完成率基线"""
    print("=" * 60)
    print("角色化协作失效边界判据 (三红线)")
    print("=" * 60)
    cases = [
        ("多角色(研+写+审)", 0.20, 0.10, 0.10),
        ("混合任务(单+多+知)", 0.40, 0.20, 0.30),
        ("开放探索(头脑风暴)", 0.60, 0.40, 0.50),
        ("单角色FAQ", 0.10, 0.05, 0.05),
    ]
    print(f"{'任务':<22} {'Goal抽象':<8} {'任务开放':<8} {'并行率':<8} {'判决':<14}")
    print("-" * 64)
    for name, ga, to, pr in cases:
        c = CrewSuitabilityChecker(ga, to, pr)
        v = c.verdict()
        print(f"{name:<20} {ga:.0%}{'':<5} {to:.0%}{'':<5} {pr:.0%}{'':<5} {v['verdict']}")
        print(f"{'':<46} 替代: {v.get('替代', '')[:30]}")
    print()
    print("=" * 60)
    print("三类任务完成率基线 (裸Crew/手补/混合/完整)")
    print("=" * 60)
    baselines = [
        TaskCompletionBaseline("单角色任务(FAQ)", 0.73, 0.79, 0.92, 0.94),
        TaskCompletionBaseline("多角色任务(研+写+审)", 0.73, 0.85, 0.88, 0.89),
        TaskCompletionBaseline("混合任务(单+多+知)", 0.67, 0.79, 0.88, 0.89),
    ]
    print(f"{'任务类型':<24} {'裸Crew':<8} {'手补':<8} {'混合':<8} {'完整':<8}")
    print("-" * 60)
    for b in baselines:
        s = b.summary()
        print(f"{s['task_type']:<22} {s['裸Crew']:<8} {s['手补Crew']:<8} {s['混合谱系']:<8} {s['完整harness']:<8}")
    print("=" * 60)
    print("结论: 单角色73%裸Crew够(开销不划算用纯编排), 多角色73%裸崩混合88%,")
    print("      开放探索 弃Crew转编排或自研(2.15决策树)")
    print("      CrewAI不可替代价值: 多角色分工任务协作显式可控")
    print("      (Role+Task+Crew三层显式契约 > AutoGen对话自然涌现)")
    print("      代价: Role抽象失指导+Task抽象失灵活+Crew协作僵化+层级错配")
    print("      CrewAI vs AutoGen = 显式可控 vs 自然涌现 的哲学分野")
    print("      链/图/检索/对话/角色/自研 是2.15决策树六档选择 按任务特征升档")

if __name__ == "__main__":
    main()
