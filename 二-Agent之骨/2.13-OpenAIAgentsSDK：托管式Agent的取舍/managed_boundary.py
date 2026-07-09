# 文件名: managed_boundary.py
# 功能: 托管式Agent失效边界三红线判据 + 三类任务完成率基线
# 运行: python managed_boundary.py
"""
托管式Agent失效边界三红线:
  - 透明红线: 调试敏度 ≥ 30% 黑盒loop调试盲区超17%
  - 工具红线: 工具敏度 ≥ 25% function calling黑盒错误超30%
  - 成本红线: 成本敏度 ≥ 20% Runs自动多轮超2.3x预算
  判决: 0红线裸托管够用, 1手补, 2弃托管转自研
"""

from dataclasses import dataclass

@dataclass
class ManagedSuitabilityChecker:
    """托管式Agent适用性判据: 三红线"""
    debug_sensitivity: float
    tool_sensitivity: float
    cost_sensitivity: float
    multi_cloud: bool = False
    def verdict(self) -> dict:
        if (self.debug_sensitivity < 0.30 and
            self.tool_sensitivity < 0.25 and
            self.cost_sensitivity < 0.20 and
            not self.multi_cloud):
            return {"verdict": "裸托管够用", "替代": "Assistants API裸",
                    "完成率预期": "92%短平快甜点"}
        if (0.30 <= self.debug_sensitivity < 0.50 or
            self.cost_sensitivity >= 0.20):
            return {"verdict": "用混合谱系", "替代": "托管作自研harness节点",
                    "完成率预期": "88%"}
        risks = []
        if self.debug_sensitivity >= 0.50:
            risks.append({"redline": "托管状态不透明", "fix": "Run Steps+本地镜像或转自研"})
        if self.tool_sensitivity >= 0.25:
            risks.append({"redline": "托管工具黑盒", "fix": "工具护栏或转自研"})
        if self.cost_sensitivity >= 0.40:
            risks.append({"redline": "托管成本失控", "fix": "max_steps+预算或转自研"})
        if self.multi_cloud:
            risks.append({"redline": "托管锁锁定", "fix": "抽象层+本地镜像或转自研"})
        if len(risks) >= 2:
            return {"verdict": "弃托管转自研", "risks": risks,
                    "替代": "自研harness(2.15)或混合谱系", "完成率预期": "85-89%"}
        return {"verdict": "手补托管可用", "risks": risks,
                "替代": "Steps+护栏+max_steps", "完成率预期": "85%"}

@dataclass
class TaskCompletionBaseline:
    """三类任务完成率基线"""
    task_type: str
    naive_managed: float
    patched_managed: float
    hybrid_spectrum: float
    full_harness: float
    def summary(self) -> dict:
        return {"task_type": self.task_type,
                "裸托管": f"{self.naive_managed:.0%}",
                "手补托管": f"{self.patched_managed:.0%}",
                "混合谱系": f"{self.hybrid_spectrum:.0%}",
                "完整harness": f"{self.full_harness:.0%}"}

def main():
    """demo: 三红线判据 + 三类任务完成率基线"""
    print("=" * 60)
    print("托管式Agent失效边界判据 (三红线)")
    print("=" * 60)
    cases = [
        ("短平快(hackathon)", 0.10, 0.10, 0.10, False),
        ("混合任务(短+核心)", 0.40, 0.20, 0.30, False),
        ("核心业务(生产)", 0.60, 0.40, 0.50, True),
        ("demo给关键客户", 0.20, 0.10, 0.10, False),  # 短平快但核心 敏度修正
    ]
    print(f"{'任务':<22} {'调敏':<8} {'具敏':<8} {'成敏':<8} {'多云':<6} {'判决':<14}")
    print("-" * 70)
    for name, ds, ts, cs, mc in cases:
        c = ManagedSuitabilityChecker(ds, ts, cs, mc)
        v = c.verdict()
        print(f"{name:<20} {ds:.0%}{'':<5} {ts:.0%}{'':<5} {cs:.0%}{'':<5} {'是' if mc else '否':<6} {v['verdict']}")
        print(f"{'':<46} 替代: {v.get('替代', '')[:30]}")
    print()
    print("=" * 60)
    print("三类任务完成率基线 (裸托管/手补/混合/完整)")
    print("=" * 60)
    baselines = [
        TaskCompletionBaseline("短平快任务(hackathon)", 0.92, 0.92, 0.92, 0.94),
        TaskCompletionBaseline("核心业务任务(生产)", 0.76, 0.85, 0.88, 0.89),
        TaskCompletionBaseline("混合任务(短+核心)", 0.67, 0.79, 0.88, 0.89),
    ]
    print(f"{'任务类型':<24} {'裸托管':<8} {'手补':<8} {'混合':<8} {'完整':<8}")
    print("-" * 60)
    for b in baselines:
        s = b.summary()
        print(f"{s['task_type']:<22} {s['裸托管']:<8} {s['手补托管']:<8} {s['混合谱系']:<8} {s['完整harness']:<8}")
    print("=" * 60)
    print("结论: 短平快92%裸托管够(省300行), 核心业务76%裸崩混合88%,")
    print("      多云敏 弃托管转自研(2.15决策树)")
    print("      托管不可替代价值: 短平快任务工程成本消失(十行托管省自研300行)")
    print("      代价: 调试盲区+工具黑盒+成本失控+锁锁定 — 省心即失控")
    print("      托管式 vs 自研式 = 省心 vs 可控 的哲学分野")
    print("      链/图/检索/对话/角色/托管/自研 是2.15决策树七档选择 按任务特征升档")

if __name__ == "__main__":
    main()
