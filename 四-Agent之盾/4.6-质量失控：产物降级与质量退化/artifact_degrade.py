# 文件名: artifact_degrade.py
# 功能: Agent 生成低质量产物止于检测缺失致降级率 100%
# 运行: python artifact_degrade.py

"""产物降级阶：低质量产物，崩在检测漏。"""

import random

random.seed(42)


def mock_low_quality_artifact(artifact_id: int, inject_degrade: bool = False) -> dict:
    if inject_degrade:
        return {"id": artifact_id, "quality": 0.3, "threshold": 0.8, "degraded": True}
    return {"id": artifact_id, "quality": 0.9, "threshold": 0.8, "degraded": False}


def detect_quality(quality: float, threshold: float = 0.8) -> bool:
    return quality >= threshold


def run_artifact_degrade(artifact_id: int) -> dict:
    r = mock_low_quality_artifact(artifact_id, inject_degrade=random.random() < 1.0)
    if detect_quality(r["quality"], r["threshold"]):
        return {"accepted": True, "reason": "质量达标", "degraded": False}
    return {"accepted": False, "reason": "产物降级", "degraded": True}


def simulate_degrade(n: int = 50) -> dict:
    accepted = 0
    degraded = 0
    for i in range(n):
        r = run_artifact_degrade(i)
        if r["accepted"]:
            accepted += 1
        else:
            degraded += 1
    return {"accepted_rate": accepted / n, "degraded_rate": degraded / n, "n": n}


def main():
    r = simulate_degrade(50)
    print("产物降级阶仿真结果（n=50）:")
    print(f"  接受率: {r['accepted_rate']:.0%}（质量达标即接受）")
    print(f"  降级率: {r['degraded_rate']:.0%}（产物质量低于阈值）")
    print(f"  崩溃模式: 检测漏——产物降级无检测即弃无从防患")


if __name__ == "__main__":
    main()
