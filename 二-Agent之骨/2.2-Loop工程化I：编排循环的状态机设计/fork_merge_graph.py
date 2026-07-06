# 文件名: fork_merge_graph.py
# 功能: 状态图（分叉/合并/回跳）的扩展能力演示
# 运行: python fork_merge_graph.py

"""从状态机到状态图：分叉、合并、回跳。

状态图允许多入口多出口、环（回跳）。
分叉: plan 同时分发到多个 act
合并: merge 等待所有分叉完成
回跳: observe 回跳到 plan（反思）
教学版，模拟状态图执行。
"""
from dataclasses import dataclass, field
import random

random.seed(7)

@dataclass
class ForkNode:
    name: str
    branches: list[str] = field(default_factory=list)
    results: dict[str, str] = field(default_factory=dict)

    def execute(self) -> dict:
        """并发执行所有分支（模拟）。"""
        for b in self.branches:
            # 模拟分支成功/失败
            ok = random.random() > 0.2
            self.results[b] = "ok" if ok else "error"
        return self.results

@dataclass
class MergeNode:
    """合并节点：等待所有分叉完成，缺一不可。"""
    required: list[str]
    collected: dict[str, str] = field(default_factory=dict)
    timeout_sec: float = 30.0

    def collect(self, branch: str, result: str) -> bool:
        self.collected[branch] = result
        return self.is_complete()

    def is_complete(self) -> bool:
        return all(r in self.collected for r in self.required)

    def quality(self) -> str:
        if not self.is_complete():
            return "不完整"
        if any("error" in v for v in self.collected.values()):
            return "部分失败"
        return "齐全"

@dataclass
class ReflectiveLoop:
    """带回跳的状态图：observe 可回跳到 plan。"""
    max_reflections: int = 2
    reflections: int = 0
    trajectory: list[str] = field(default_factory=list)

    def step(self, state: str, need_reflection: bool) -> str:
        self.trajectory.append(state)
        if state == "observe" and need_reflection:
            self.reflections += 1
            if self.reflections <= self.max_reflections:
                return "plan"  # 回跳
            return "escalate"  # 反思超限
        if state == "plan":
            return "act"
        if state == "act":
            return "observe"
        if state == "observe":
            return "finish"
        return state

def main():
    print("=" * 64)
    print("状态图扩展：分叉 / 合并 / 回跳")
    print("=" * 64)

    # 分叉
    print("\n【分叉】plan 同时分发 2 个子任务:")
    fork = ForkNode("plan", branches=["act_A", "act_B"])
    results = fork.execute()
    for b, r in results.items():
        print(f"  {b}: {r}")

    # 合并
    print("\n【合并】等待所有分叉完成:")
    merge = MergeNode(required=["act_A", "act_B"])
    for b, r in results.items():
        merge.collect(b, r)
    print(f"  合并质量: {merge.quality()}")
    print(f"  是否完整: {merge.is_complete()}")

    # 回跳（反思）
    print("\n【回跳】反思后从 observe 回跳到 plan:")
    loop = ReflectiveLoop(max_reflections=2)
    states = ["plan", "act", "observe"]  # 第一轮
    next_s = ""
    for s in states:
        next_s = loop.step(s, need_reflection=(s == "observe" and loop.reflections < 2))
        print(f"  {s} → {next_s}")
    # 回跳后第二轮
    states2 = ["plan", "act", "observe"]
    for s in states2:
        need_r = (s == "observe" and loop.reflections < 2)
        next_s = loop.step(s, need_reflection=need_r)
        print(f"  {s} → {next_s}")
    print(f"  反思次数: {loop.reflections}（上限 {loop.max_reflections}）")
    print(f"  轨迹: {' → '.join(loop.trajectory)}")

    print("\n结论：状态图通过分叉合并回跳覆盖非线性 loop，")
    print("      LangGraph 把状态图实现为一等公民，调试需分布式追踪。")

if __name__ == "__main__":
    main()
