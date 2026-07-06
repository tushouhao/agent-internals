# 文件名: three_layers.py
# 功能: 上下文三层结构（指令/轨迹/工具）的占比与重要性量化
# 运行: python three_layers.py

"""上下文三层结构：指令/轨迹/工具的占比与重要性。

指令层: 任务描述/约束/角色，全程不可丢
轨迹层: think/act 历史，可摘要/截断
工具层: 工具返回结果，最占窗口，可抽取/引用
教学版，模拟 80 步任务的三层分布。
"""
import random
from dataclasses import dataclass, field

random.seed(2026)

@dataclass
class ThreeLayerContext:
    instruction_tokens: int = 500       # 指令层固定
    trajectory: list[dict] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)
    window: int = 32000

    def simulate_steps(self, steps: int):
        for i in range(steps):
            self.trajectory.append({"step": i, "content": f"think+act 第{i}步", "tokens": 120})
            self.tool_results.append({"step": i, "tool": "read_file",
                                      "content": "x" * random.randint(2000, 5000),
                                      "tokens": random.randint(500, 1250)})

    def layer_tokens(self) -> dict:
        return {
            "instruction": self.instruction_tokens,
            "trajectory": sum(m["tokens"] for m in self.trajectory),
            "tool": sum(m["tokens"] for m in self.tool_results),
        }

    def layer_ratios(self) -> dict:
        total = sum(self.layer_tokens().values())
        if total == 0:
            return {"instruction": 0, "trajectory": 0, "tool": 0}
        lt = self.layer_tokens()
        return {k: v / total for k, v in lt.items()}

    def instruction_lost_by_naive_truncate(self) -> bool:
        """naive 截断按 FIFO，最先丢指令层。"""
        total = sum(self.layer_tokens().values())
        return total > self.window  # 超窗口即丢最早（指令）

def main():
    print("=" * 64)
    print("上下文三层结构：占比与重要性（80 步任务）")
    print("=" * 64)
    ctx = ThreeLayerContext()
    ctx.simulate_steps(80)
    lt = ctx.layer_tokens()
    lr = ctx.layer_ratios()
    print(f"\n各层 token 数:")
    for k, v in lt.items():
        print(f"  {k:<14}: {v:>7} ({lr[k]:.1%})")
    print(f"  {'总计':<14}: {sum(lt.values()):>7} / {ctx.window}")
    print(f"\n重要性排序（压缩顺序反向）:")
    print(f"  1. 指令层 {lt['instruction']} token — 全程不可丢（最重要）")
    print(f"  2. 轨迹层 {lt['trajectory']} token — 可摘要/截断")
    print(f"  3. 工具层 {lt['tool']} token — 可抽取/引用（最占窗口）")
    print(f"\nnaive 截断最先丢哪层?")
    print(f"  指令层丢失: {'是 ← 任务跑偏根源' if ctx.instruction_lost_by_naive_truncate() else '否'}")
    print(f"  naive 按 FIFO 丢最早，指令层恰是最早的")

if __name__ == "__main__":
    main()
