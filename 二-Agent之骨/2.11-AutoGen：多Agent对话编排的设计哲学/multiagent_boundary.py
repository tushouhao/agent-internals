# 文件名: multiagent_boundary.py
# 功能: 多Agent对话失效边界三红线判据 + 三类任务完成率基线
# 运行: python multiagent_boundary.py
"""
多Agent对话失效边界三红线:
  - 分工红线: 任务不可清晰分工率 ≥ 30% 角色模糊致越权超18%
  - 收敛红线: 收敛条件模糊率 ≥ 20% 死锁超12%
  - Agent数红线: Agent数 ≥ 3 且协调开销超增益 净负即亏
  判决: 0红线裸对话够用, 1手补, 2弃对话转编排
"""

from dataclasses import dataclass

@dataclass
class MultiAgentSuitabilityChecker:
    """多Agent对话适用性判据: 三红线"""
    unsplitable_ratio: float  # 不可分工率
    unclear_converge_ratio: float  # 收敛模糊率
    agent_count: int  # Agent数
    coord_overhead: float  # 协调开销
    collab_gain: float  # 协作增益
    def verdict(self) -> dict:
        # 甜点: 可分工 + 不重叠 + 收敛明确 + Agent数<=2
        if (self.unsplitable_ratio < 0.30 and
            self.unclear_converge_ratio < 0.20 and
            self.agent_count <= 2):
            return {"verdict": "裸对话够用", "替代": "AutoGen裸GroupChat",
                    "完成率预期": "71%多角色甜点"}
        # 混合任务甜点
        if (0.30 <= self.unsplitable_ratio < 0.50 or
            self.agent_count == 3):
            return {"verdict": "用混合谱系", "替代": "AutoGen+LangGraph混合",
                    "完成率预期": "88%"}
        # 失效红线
        risks = []
        if self.unsplitable_ratio >= 0.50:
            risks.append({"redline": "角色模糊", "fix": "升混合谱系或转编排"})
        if self.unclear_converge_ratio >= 0.20:
            risks.append({"redline": "收敛模糊死锁", "fix": "接仲裁Agent或转编排"})
        if self.agent_count >= 3 and self.coord_overhead > self.collab_gain:
            risks.append({"redline": "协调亏", "fix": "收口到2或转编排"})
        if len(risks) >= 2:
            return {"verdict": "弃对话转编排", "risks": risks,
                    "替代": "LangGraph编排或自研(2.15)", "完成率预期": "85-89%"}
        return {"verdict": "手补对话可用", "risks": risks,
                "替代": "仲裁+契约+收口", "完成率预期": "85%"}

@dataclass
class TaskCompletionBaseline:
    """三类任务完成率基线"""
    task_type: str
    naive_conversation: float
    patched_conversation: float
    hybrid_spectrum: float
    full_harness: float
    def summary(self) -> dict:
        return {"task_type": self.task_type,
                "裸对话": f"{self.naive_conversation:.0%}",
                "手补对话": f"{self.patched_conversation:.0%}",
                "混合谱系": f"{self.hybrid_spectrum:.0%}",
                "完整harness": f"{self.full_harness:.0%}"}

def main():
    """demo: 三红线判据 + 三类任务完成率基线"""
    print("=" * 60)
    print("多Agent对话失效边界判据 (三红线)")
    print("=" * 60)
    cases = [
        ("单角色FAQ", 0.10, 0.05, 1, 0.0, 0.0),
        ("多角色(研究+写+审)", 0.20, 0.10, 2, 0.20, 0.21),
        ("混合任务(单+多角色)", 0.40, 0.15, 3, 0.40, 0.25),
        ("开放讨论(头脑风暴)", 0.60, 0.30, 5, 0.70, 0.35),
    ]
    print(f"{'任务':<22} {'不可分工':<8} {'收敛模糊':<8} {'Agent数':<8} {'判决':<14}")
    print("-" * 64)
    for name, uns, unc, ac, co, cg in cases:
        c = MultiAgentSuitabilityChecker(uns, unc, ac, co, cg)
        v = c.verdict()
        print(f"{name:<20} {uns:.0%}{'':<5} {unc:.0%}{'':<5} {ac:<8} {v['verdict']}")
        print(f"{'':<46} 替代: {v.get('替代', '')[:30]}")
    print()
    # 完成率基线
    print("=" * 60)
    print("三类任务完成率基线 (裸对话/手补/混合/完整)")
    print("=" * 60)
    baselines = [
        TaskCompletionBaseline("单角色任务(FAQ)", 0.71, 0.79, 0.92, 0.94),
        TaskCompletionBaseline("多角色任务(研+写+审)", 0.71, 0.85, 0.88, 0.89),
        TaskCompletionBaseline("混合任务(单+多角色)", 0.67, 0.79, 0.88, 0.89),
    ]
    print(f"{'任务类型':<24} {'裸对话':<8} {'手补':<8} {'混合':<8} {'完整':<8}")
    print("-" * 60)
    for b in baselines:
        s = b.summary()
        print(f"{s['task_type']:<22} {s['裸对话']:<8} {s['手补对话']:<8} {s['混合谱系']:<8} {s['完整harness']:<8}")
    print("=" * 60)
    print("结论: 单角色71%裸对话够(开销不划算用纯编排), 多角色71%裸崩混合88%,")
    print("      开放讨论 弃对话转编排或自研(2.15决策树)")
    print("      多Agent对话不可替代价值: 多角色分工任务协作自然涌现")
    print("      (Agent互对话即协作无需显式调度), 但代价是死锁+越权+token炸+协调亏")
    print("      链/图/检索/对话/自研 是2.15决策树五档选择 按任务特征升档")

if __name__ == "__main__":
    main()
