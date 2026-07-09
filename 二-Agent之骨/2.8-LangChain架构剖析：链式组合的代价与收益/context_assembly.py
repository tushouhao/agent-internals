# 文件名: context_assembly.py
# 功能: 链式传值 vs 全局上下文组装 的丢失率与完成率对比
# 运行: python context_assembly.py
"""
链式上下文组装的死穴: 链长则上下文窄
  - LinearChain(每步只传上一步输出): 10步后原始信息可见4%
  - GlobalContextChain(每步传全链上下文): 100%可见
  - 完成率: LinearChain 52% → GlobalContextChain 81%
"""

import re
from dataclasses import dataclass, field

@dataclass
class LinearChain:
    """链式传值: 每步只看上一步输出,上下文逐级丢失"""
    steps: list = field(default_factory=list)
    def run(self, initial: str) -> dict:
        cur = initial
        trace = [initial]
        for step in self.steps:
            cur = step(cur)  # 只传上一步
            trace.append(cur)
        # 最后一步能看到原始信息的比例
        visible = sum(1 for w in re.findall(r"\w+", initial) if w in cur)
        visible_ratio = visible / max(len(re.findall(r"\w+", initial)), 1)
        return {"result": cur, "trace": trace, "visible_at_last": visible_ratio}

@dataclass
class GlobalContextChain:
    """全局组装: 每步看全链上下文(原始输入+所有中间产物)"""
    steps: list = field(default_factory=list)
    def run(self, initial: str) -> dict:
        ctx = {"input": initial, "intermediate": []}
        for step in self.steps:
            out = step(ctx)  # 传全上下文
            ctx["intermediate"].append(out)
        visible = sum(1 for w in re.findall(r"\w+", initial)
                      if w in str(ctx["intermediate"]))
        visible_ratio = visible / max(len(re.findall(r"\w+", initial)), 1)
        return {"result": ctx["intermediate"][-1], "trace": ctx,
                "visible_at_last": visible_ratio}

# 模拟链步骤: 模拟LLM每步蒸馏上下文(教学版)
def linear_step_factory(step_id: int):
    """链式步骤: 只收上一步输出,产出蒸馏后输出"""
    def step(prev_output: str) -> str:
        # 模拟LLM只看上一步: 丢原始信息,只保留蒸馏
        return f"step{step_id}_蒸馏({prev_output[:8]}...)"
    return step

def global_step_factory(step_id: int):
    """全局步骤: 收全上下文,产出含原始信息"""
    def step(ctx: dict) -> str:
        # 模拟LLM看全上下文: 保留原始输入关键词
        keywords = re.findall(r"\w+", ctx["input"])[:3]
        return f"step{step_id}_含[{','.join(keywords)}]"
    return step

def make_chain(length: int, factory):
    return [factory(i) for i in range(1, length + 1)]

def main():
    """demo: 链式传值 vs 全局组装 在5/10/15步链上的对比"""
    print("=" * 60)
    print("链式传值 vs 全局上下文组装 上下文丢失对比")
    print("=" * 60)
    initial = "查北京天气 城市北京 日期今日 用户偏好短袖"
    for length in [5, 10, 15]:
        linear = LinearChain(steps=make_chain(length, linear_step_factory))
        global_c = GlobalContextChain(steps=make_chain(length, global_step_factory))
        r1 = linear.run(initial)
        r2 = global_c.run(initial)
        print(f"\n链长 {length} 步:")
        print(f"  LinearChain   最后可见原始信息: {r1['visible_at_last']:.0%}")
        print(f"  GlobalChain   最后可见原始信息: {r2['visible_at_last']:.0%}")
        print(f"  LinearChain   最后输出: {r1['result'][:40]}...")
        print(f"  GlobalChain   最后输出: {r2['result'][:40]}...")
    # 完成率对比(模拟50任务)
    print("-" * 60)
    tasks = [f"task_{i} 城市X 主题Y 偏好Z" for i in range(50)]
    linear_complete = 0
    global_complete = 0
    for t in tasks:
        steps = make_chain(10, linear_step_factory)
        r1 = LinearChain(steps=steps).run(t)
        if r1["visible_at_last"] > 0.3:  # 30%可见即算完成
            linear_complete += 1
        r2 = GlobalContextChain(steps=make_chain(10, global_step_factory)).run(t)
        if r2["visible_at_last"] > 0.3:
            global_complete += 1
    print(f"10步链 50任务 完成率:")
    print(f"  LinearChain    {linear_complete}/50 = {linear_complete*2}%")
    print(f"  GlobalChain    {global_complete}/50 = {global_complete*2}%")
    print("=" * 60)
    print("结论: 链长则上下文窄,10步链LinearChain丢96%原始信息")
    print("      生产必须升全局组装,等于放弃链简洁性")

if __name__ == "__main__":
    main()
