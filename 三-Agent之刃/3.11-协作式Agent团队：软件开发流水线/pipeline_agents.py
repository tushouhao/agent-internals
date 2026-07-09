# 文件名: pipeline_agents.py
# 功能: 编码/测试/部署串三 Agent，接口契约 JSON 链式传递，止于接口失配
# 运行: python pipeline_agents.py

"""流水线阶：三 Agent 串行，接口契约传递，崩在失配漏出。"""

import random
import json

random.seed(42)


def mock_coding_agent(requirement: str) -> dict:
    """编码 Agent：需求→ code.json 契约。"""
    return {
        "module": f"mod_{abs(hash(requirement)) % 1000}",
        "entry": "main",
        "deps": ["dep_a", "dep_b"],
        "api": {"run": "()->str"},
    }


def mock_test_agent(code_contract: dict) -> dict:
    """测试 Agent：code.json→ test.json 契约。
    失配指测试调用了 code_contract 不存在的 api。
    """
    expected_apis = set(code_contract.get("api", {}).keys())
    test_calls = ["run", "validate", "teardown"]
    mismatches = [c for c in test_calls if c not in expected_apis]
    return {
        "test_calls": test_calls,
        "mismatches": mismatches,
        "pass": len(mismatches) == 0,
    }


def mock_deploy_agent(test_contract: dict) -> dict:
    """部署 Agent：test.json→ deploy.json 契约。"""
    if not test_contract["pass"]:
        return {"deployed": False, "reason": "测试未过"}
    return {"deployed": True, "env": "prod"}


def run_pipeline(requirement: str) -> dict:
    """流水线三 Agent 串行。"""
    code = mock_coding_agent(requirement)
    test = mock_test_agent(code)
    deploy = mock_deploy_agent(test)
    return {
        "completed": deploy["deployed"],
        "mismatches": test["mismatches"],
        "has_mismatch": len(test["mismatches"]) > 0,
    }


def simulate_pipeline(n: int = 50) -> dict:
    """流水线阶仿真：50 任务交付率 + 失配率。"""
    completed = 0
    mismatch = 0
    for i in range(n):
        r = run_pipeline(f"需求_{i}")
        if r["completed"]:
            completed += 1
        if r["has_mismatch"]:
            mismatch += 1
    return {
        "completed_rate": completed / n,
        "mismatch_rate": mismatch / n,
        "n": n,
    }


def main():
    """流水线阶 demo。"""
    r = simulate_pipeline(50)
    print("流水线阶仿真结果（n=50）:")
    print(f"  交付率: {r['completed_rate']:.0%}（三 Agent 串行）")
    print(f"  接口失配率: {r['mismatch_rate']:.0%}（编码契约 vs 测试调用不对齐）")
    print(f"  崩溃模式: 接口失配漏出——测试调用了编码不提供的 api 即割裂交付")


if __name__ == "__main__":
    main()
