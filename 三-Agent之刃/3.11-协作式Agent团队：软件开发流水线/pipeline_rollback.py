# 文件名: pipeline_rollback.py
# 功能: 流水线中途崩溃分阶段回滚，止于回滚成功率
# 运行: python pipeline_rollback.py

"""流水线回滚护栏：分阶段崩溃分级回滚。"""

import random

random.seed(42)


def mock_coding(requirement: str) -> dict:
    return {"code": "ok", "pass": random.random() > 0.2}


def mock_test(code: dict) -> dict:
    return {"test": "ok", "pass": random.random() > 0.3 and code["pass"]}


def mock_deploy(test: dict) -> dict:
    return {"deploy": "ok", "pass": random.random() > 0.1 and test["pass"]}


def run_pipeline_with_rollback(requirement: str) -> dict:
    """流水线 + 分阶段回滚。"""
    artifacts = {}
    code = mock_coding(requirement)
    artifacts["code"] = code
    if not code["pass"]:
        del artifacts["code"]
        return {"completed": False, "rollback": "清编码", "artifacts": artifacts}
    test = mock_test(code)
    artifacts["test"] = test
    if not test["pass"]:
        del artifacts["test"]
        return {"completed": False, "rollback": "清测试保留编码", "artifacts": artifacts}
    deploy = mock_deploy(test)
    artifacts["deploy"] = deploy
    if not deploy["pass"]:
        del artifacts["deploy"]
        return {"completed": False, "rollback": "清部署保留编码+测试", "artifacts": artifacts}
    return {"completed": True, "rollback": "无", "artifacts": artifacts}


def simulate_rollback(n: int = 90) -> dict:
    """回滚护栏仿真：90 任务回滚成功率。"""
    completed = 0
    rollback_success = 0
    rollback_total = 0
    for i in range(n):
        r = run_pipeline_with_rollback(f"需求_{i}")
        if r["completed"]:
            completed += 1
        else:
            rollback_total += 1
            if r["artifacts"]:
                rollback_success += 1
    return {
        "completed_rate": completed / n,
        "rollback_rate": rollback_total / n,
        "rollback_success_rate": rollback_success / rollback_total if rollback_total else 1.0,
        "n": n,
    }


def main():
    """回滚护栏 demo。"""
    r = simulate_rollback(90)
    print("回滚护栏仿真结果（n=90）:")
    print(f"  交付率: {r['completed_rate']:.0%}")
    print(f"  崩溃率: {r['rollback_rate']:.0%}（流水线中途崩）")
    print(f"  回滚成功率: {r['rollback_success_rate']:.0%}（分阶段清产物）")
    print(f"  三策略: 编码崩清编码 / 测试崩清测试保编码 / 部署崩清部署保编码+测试")


if __name__ == "__main__":
    main()
