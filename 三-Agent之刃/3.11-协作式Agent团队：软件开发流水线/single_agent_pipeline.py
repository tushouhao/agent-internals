# 文件名: single_agent_pipeline.py
# 功能: 单 Agent 独揽需求→编码→测试→部署全流程，止于上下文上限
# 运行: python single_agent_pipeline.py

"""单 Agent 阶：独揽全流程，崩在上下文上限炸。"""

import random

random.seed(42)


def mock_llm(prompt: str, max_tokens: int = 2000) -> str:
    """模拟 LLM 推理：生产替换为真实 API。
    复杂需求（含「高」）每阶段耗 ~2500 token 致四阶段累加超 8000 即炸。
    """
    if "高" in prompt:
        return "x" * 10000  # 粗估 2500 token
    return "x" * 2000  # 粗估 500 token


def run_single_agent(requirement: str) -> dict:
    """单 Agent 独揽全流程：需求→编码→测试→部署。
    上下文上限 8k token，超即炸。
    """
    ctx_tokens = 0
    stages = ["需求", "编码", "测试", "部署"]
    artifacts = {}
    for stage in stages:
        prompt = f"{stage} 阶段处理需求: {requirement}"
        output = mock_llm(prompt, max_tokens=2000)
        ctx_tokens += len(output) // 4
        artifacts[stage] = output
        if ctx_tokens > 8000:
            return {"completed": False, "reason": "上下文上限炸", "ctx_tokens": ctx_tokens, "stage_failed": stage}
    return {"completed": True, "ctx_tokens": ctx_tokens, "artifacts": artifacts}


def simulate_single(n: int = 50) -> dict:
    """单 Agent 阶仿真：50 任务交付率。"""
    completed = 0
    ctx_blow = 0
    for i in range(n):
        req = f"需求_{i} 复杂度 {'高' if i % 2 == 0 else '中'}"
        r = run_single_agent(req)
        if r["completed"]:
            completed += 1
        else:
            ctx_blow += 1
    return {
        "completed_rate": completed / n,
        "ctx_blow_rate": ctx_blow / n,
        "n": n,
    }


def main():
    """单 Agent 阶 demo。"""
    r = simulate_single(50)
    print("单 Agent 阶仿真结果（n=50）:")
    print(f"  交付率: {r['completed_rate']:.0%}（独揽全流程）")
    print(f"  上下文炸率: {r['ctx_blow_rate']:.0%}（8k token 上限）")
    print(f"  崩溃模式: 上下文上限炸——编码+测试+部署三阶段全进一上下文超限")


if __name__ == "__main__":
    main()
