# 文件名: session_loop.py
# 功能: 单会话 ReAct 循环（推理→行动→观察），止于上下文上限炸
# 运行: python session_loop.py

"""会话内 loop 阶：单会话 ReAct 循环，崩在上下文上限炸。"""

import random

random.seed(42)


def mock_react_step(step: int, task: str) -> dict:
    """模拟 ReAct 三段：推理→行动→观察。每步耗 ~1200 token。"""
    return {
        "step": step,
        "thought": f"步{step} 推理: 分析 {task}",
        "action": f"步{step} 行动: 调用工具处理",
        "observe": f"步{step} 观察: 工具返回结果",
        "tokens": 1200,
    }


def run_session_loop(task: str, max_steps: int = 20) -> dict:
    """单会话 ReAct 循环，上下文上限 8k token，超即炸。"""
    ctx_tokens = 0
    steps_done = 0
    trace = []
    for step in range(max_steps):
        r = mock_react_step(step, task)
        ctx_tokens += r["tokens"]
        steps_done += 1
        trace.append(r)
        if ctx_tokens > 8000:
            return {"completed": False, "reason": "上下文上限炸", "steps_done": steps_done, "ctx_tokens": ctx_tokens, "trace": trace}
    return {"completed": True, "steps_done": steps_done, "ctx_tokens": ctx_tokens, "trace": trace}


def simulate_session(n: int = 50) -> dict:
    """会话内 loop 阶仿真：50 任务续跑率。"""
    completed = 0
    ctx_blow = 0
    for i in range(n):
        r = run_session_loop(f"任务_{i}", max_steps=20)
        if r["completed"]:
            completed += 1
        else:
            ctx_blow += 1
    return {"completed_rate": completed / n, "ctx_blow_rate": ctx_blow / n, "continuation_rate": 0.0, "n": n}


def main():
    """会话内 loop 阶 demo。"""
    r = simulate_session(50)
    print("会话内 loop 阶仿真结果（n=50）:")
    print(f"  完成率: {r['completed_rate']:.0%}（单会话 ReAct 循环毕）")
    print(f"  上下文炸率: {r['ctx_blow_rate']:.0%}（8k token 上限）")
    print(f"  续跑率: {r['continuation_rate']:.0%}（崩即从头重跑切片全丢）")
    print(f"  崩溃模式: 上下文上限炸——长程任务必炸无可切片归档")


if __name__ == "__main__":
    main()
