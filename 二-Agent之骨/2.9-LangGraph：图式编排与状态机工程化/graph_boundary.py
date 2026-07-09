# 文件名: graph_boundary.py
# 功能: 图式抽象失效边界四红线判据(步数/分支/跨度/开放度) + 三类任务完成率基线
# 运行: python graph_boundary.py
"""
图式抽象失效边界四红线:
  - 5步内单分支: 链式甜点, 图式过载 → 用LangChain裸链
  - 6-50步多分支: 图式甜点 → 用LangGraph + checkpointer + gate
  - 50步以上: TypedDict契约崩溃 → 弃图转自研(2.15)
  - 开放探索: State字段无法预声明 → 弃图转自研
"""

from dataclasses import dataclass, field

@dataclass
class GraphSuitabilityChecker:
    """图式抽象适用性判据: 四红线"""
    step_count: int
    branch_count: int
    span: str  # "single_turn" / "multi_turn" / "cross_day"
    openness: str  # "closed" / "semi_open" / "open"
    def verdict(self) -> dict:
        risks = []
        benefits = []
        # 链式甜点: 5步内单分支
        if self.step_count <= 5 and self.branch_count <= 1:
            return {"verdict": "用链不用图", "reason": "甜点内图式过载",
                    "替代": "LangChain裸链", "完成率预期": "78%裸链够用"}
        # 图式甜点: 6-50步多分支
        if 6 <= self.step_count <= 50 and self.branch_count >= 2:
            benefits.append({"甜点": "中等以上长程, 图式六短板全补"})
        # 图式失效红线
        if self.step_count > 50:
            risks.append({"redline": "步数过多", "fix": "TypedDict契约崩溃, 转自研"})
        if self.openness == "open":
            risks.append({"redline": "开放探索", "fix": "State字段无法预声明, 转自研"})
        if self.span == "cross_day" and self.step_count > 30:
            risks.append({"redline": "超长跨日", "fix": "升PostgresSaver或自研"})
        if len(risks) >= 2:
            return {"verdict": "弃图转自研", "risks": risks,
                    "替代": "自研harness(2.15)", "完成率预期": "89%自研"}
        if benefits:
            return {"verdict": "用图式", "benefits": benefits,
                    "替代": "LangGraph + checkpointer + gate", "完成率预期": "88%手补图"}
        return {"verdict": "用链或图皆可", "risks": risks, "benefits": benefits,
                "替代": "按团队熟悉度选", "完成率预期": "79-88%"}

@dataclass
class TaskCompletionBaseline:
    """三类任务完成率基线(裸链/裸图/手补图/完整harness)"""
    task_type: str
    naive_chain: float
    naive_graph: float
    patched_graph: float
    full_harness: float
    def summary(self) -> dict:
        return {"task_type": self.task_type,
                "裸链": f"{self.naive_chain:.0%}",
                "裸图": f"{self.naive_graph:.0%}",
                "手补图": f"{self.patched_graph:.0%}",
                "完整harness": f"{self.full_harness:.0%}"}

def main():
    """demo: 四红线判据 + 三类任务完成率基线"""
    print("=" * 60)
    print("图式抽象失效边界判据 (四红线)")
    print("=" * 60)
    cases = [
        ("甜点(demo/POC)", 3, 1, "single_turn", "closed"),
        ("中等(生产单轮)", 10, 3, "multi_turn", "semi_open"),
        ("长程(跨日多分支)", 50, 5, "cross_day", "semi_open"),
        ("超长(开放探索)", 80, 10, "cross_day", "open"),
        ("步少但分支极多", 5, 20, "single_turn", "closed"),  # 路由决策任务
    ]
    print(f"{'任务':<20} {'步数':<6} {'分支':<6} {'跨度':<14} {'开放':<10} {'判决':<14}")
    print("-" * 76)
    for name, step, branch, span, openness in cases:
        checker = GraphSuitabilityChecker(step, branch, span, openness)
        v = checker.verdict()
        print(f"{name:<18} {step:<6} {branch:<6} {span:<14} {openness:<10} {v['verdict']:<14}")
        print(f"{'':<44} 替代: {v.get('替代', '')[:30]}")
    print()
    # 完成率基线表
    print("=" * 60)
    print("三类任务完成率基线 (裸链/裸图/手补图/完整harness)")
    print("=" * 60)
    baselines = [
        TaskCompletionBaseline("甜点(3步单分支)", 0.78, 0.73, 0.79, 0.82),
        TaskCompletionBaseline("中等(10步多分支跨轮)", 0.41, 0.81, 0.88, 0.88),
        TaskCompletionBaseline("长程(50步多分支跨日)", 0.09, 0.73, 0.88, 0.89),
    ]
    print(f"{'任务类型':<28} {'裸链':<8} {'裸图':<8} {'手补图':<10} {'完整':<10}")
    print("-" * 60)
    for b in baselines:
        s = b.summary()
        print(f"{s['task_type']:<26} {s['裸链']:<8} {s['裸图']:<8} {s['手补图']:<10} {s['完整harness']:<10}")
    print("=" * 60)
    print("结论: 甜点用链(78%), 中等以上用图(88%), 超长/开放转自研(89%)")
    print("      裸图81%/73%比裸链41%/9%翻倍/八倍, 手补图追完整harness")
    print("      链/图/自研是2.15决策树三档选择, 按任务特征升档")

if __name__ == "__main__":
    main()
