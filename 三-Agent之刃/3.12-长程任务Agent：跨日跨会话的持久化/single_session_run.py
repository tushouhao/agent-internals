# 文件名: single_session_run.py
# 功能: 单会话上下文内连跑，止于 8k token 上限即炸
# 运行: python single_session_run.py

"""单会话阶：上下文内连跑，崩在上下文上限炸。"""

import random

random.seed(42)


def mock_llm(prompt: str) -> str:
    """模拟 LLM 推理：每步耗 ~1200 token。"""
    return "x" * 4800


def run_single_session(task: str, max_steps: int = 20) -> dict:
    """单会话内连跑，上下文上限 8k token，超即炸。"""
    ctx_tokens = 0
    steps_done = 0
    for step in range(max_steps):
        output = mock_llm(f"步{step} 处理 {task}")
        ctx_tokens += len(output) // 4
        steps_done += 1
        if ctx_tokens > 8000:
            return {"completed": False, "reason": "上下文上限炸", "steps_done": steps_done, "ctx_tokens": ctx_tokens}
    return {"completed": True, "steps_done": steps_done, "ctx_tokens": ctx_tokens}


def simulate_single(n: int = 50) -> dict:
    """单会话阶仿真：50 任务续跑率。"""
    completed = 0
    ctx_blow = 0
    for i in range(n):
        r = run_single_session(f"任务_{i}", max_steps=20)
        if r["completed"]:
            completed += 1
        else:
            ctx_blow += 1
    return {
        "completed_rate": completed / n,
        "ctx_blow_rate": ctx_blow / n,
        "continuation_rate": 0.0,
        "n": n,
    }


def main():
    """单会话阶 demo。"""
    r = simulate_single(50)
    print("单会话阶仿真结果（n=50）:")
    print(f"  完成率: {r['completed_rate']:.0%}（上下文内连跑毕）")
    print(f"  上下文炸率: {r['ctx_blow_rate']:.0%}（8k token 上限）")
    print(f"  续跑率: {r['continuation_rate']:.0%}（崩即从头重跑浪费）")
    print(f"  崩溃模式: 上下文上限炸——长程任务必炸无可续跑")


if __name__ == "__main__":
    main()
