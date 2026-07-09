# 文件名: param_hallucination.py
# 功能: LLM 生成工具参数幻觉止于校验缺失致调用率 0%
# 运行: python param_hallucination.py

"""参数幻觉阶：LLM 生成参数，崩在校验漏。"""

import random

random.seed(42)


def mock_llm_gen_params(task: str, inject_hallucination: bool = False) -> dict:
    if inject_hallucination:
        return {"task": task, "params": {"path": 123}, "hallucinated": True}
    return {"task": task, "params": {"path": "/tmp/file"}, "hallucinated": False}


def validate_params(params: dict, schema: dict) -> bool:
    for key, expected_type in schema.items():
        if key not in params:
            return False
        if not isinstance(params[key], expected_type):
            return False
    return True


def run_param_hallucination(task: str) -> dict:
    r = mock_llm_gen_params(task, inject_hallucination=random.random() < 1.0)
    schema = {"path": str}
    if not validate_params(r["params"], schema):
        return {"called": False, "reason": "参数幻觉", "hallucinated": True}
    return {"called": True, "reason": "参数合法", "hallucinated": False}


def simulate_hallucination(n: int = 50) -> dict:
    called = 0
    hallucinated = 0
    for i in range(n):
        r = run_param_hallucination(f"任务_{i}")
        if r["called"]:
            called += 1
        else:
            hallucinated += 1
    return {"called_rate": called / n, "hallucinated_rate": hallucinated / n, "n": n}


def main():
    r = simulate_hallucination(50)
    print("参数幻觉阶仿真结果（n=50）:")
    print(f"  调用率: {r['called_rate']:.0%}（参数幻觉即弃）")
    print(f"  幻觉率: {r['hallucinated_rate']:.0%}（LLM 生成参数类型错）")
    print(f"  崩溃模式: 校验漏——参数幻觉无校验即弃无从防患")


if __name__ == "__main__":
    main()
