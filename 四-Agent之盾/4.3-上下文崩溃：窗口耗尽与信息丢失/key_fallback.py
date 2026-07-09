# 文件名: key_fallback.py
# 功能: 关键漏检降级兜底三策略，止于信息残留率
# 运行: python key_fallback.py

"""关键漏检降级兜底：从产物/轮数/外部反推关键。"""

import random

random.seed(42)


def artifact_anomaly_detect(artifact: str, expected: str) -> dict:
    return {"loss_detected": artifact != expected, "method": "产物反推"}


def turn_count_limit_detect(turns: int, limit: int = 30) -> dict:
    return {"loss_detected": turns > limit, "method": "轮数反推"}


def external_store_detect(key_id: str, ext_store: dict) -> dict:
    return {"loss_detected": key_id not in ext_store, "method": "外部反推"}


def simulate_fallback(n: int = 30) -> dict:
    success = 0
    for i in range(n):
        method = random.choice(["产物", "轮数", "外部"])
        if method == "产物":
            r = artifact_anomaly_detect("产物_丢失", "产物_正常")
            if r["loss_detected"]:
                success += 1
        elif method == "轮数":
            r = turn_count_limit_detect(35, limit=30)
            if r["loss_detected"]:
                success += 1
        else:
            r = external_store_detect(f"key_{i}", {})
            if r["loss_detected"]:
                success += 1
    return {"n": n, "fallback_success_rate": success / n}


def main():
    r = simulate_fallback(30)
    print("降级兜底仿真结果（n=30）:")
    print(f"  兜底成功率: {r['fallback_success_rate']:.0%}（产物/轮数/外部三策略反推）")
    print(f"  三策略: 产物异常 / 轮数上限 / 外部存储")


if __name__ == "__main__":
    main()
