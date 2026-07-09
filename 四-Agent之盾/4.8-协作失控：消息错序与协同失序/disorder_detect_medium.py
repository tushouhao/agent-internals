# 文件名: disorder_detect_medium.py
# 功能: 失序检测基线介质三策略权衡，止于综合检测完备率
# 运行: python disorder_detect_medium.py

"""失序检测基线介质选择：本地 vs 远程 vs 云端。"""

import random

random.seed(42)


def local_baseline(baseline_data: dict) -> dict:
    return {"medium": "local", "latency_ms": 1, "durability": 0.50, "can_detect": random.random() < 0.50}


def remote_db_baseline(baseline_data: dict) -> dict:
    return {"medium": "remote", "latency_ms": 40, "durability": 0.99, "can_detect": random.random() < 0.99}


def cloud_baseline_service(baseline_data: dict) -> dict:
    return {"medium": "cloud", "latency_ms": 120, "durability": 0.999, "can_detect": random.random() < 0.999}


def choose_medium(task_criticality: str) -> str:
    if task_criticality == "生死":
        return "cloud"
    if task_criticality == "重要":
        return "remote"
    return "local"


def simulate_medium(n: int = 90) -> dict:
    stats = {"local": 0, "remote": 0, "cloud": 0}
    detects = []
    latencies = []
    for i in range(n):
        crit = random.choice(["生死", "重要", "普通"])
        medium = choose_medium(crit)
        stats[medium] += 1
        data = {"baseline_id": i}
        if medium == "local":
            r = local_baseline(data)
        elif medium == "remote":
            r = remote_db_baseline(data)
        else:
            r = cloud_baseline_service(data)
        detects.append(1 if r["can_detect"] else 0)
        latencies.append(r["latency_ms"])
    return {"stats": stats, "n": n, "avg_detect": sum(detects) / len(detects), "avg_latency": sum(latencies) / len(latencies)}


def main():
    r = simulate_medium(90)
    print("失序检测介质仿真结果（n=90）:")
    print(f"  分流: 本地 {r['stats']['local']} / 远程 {r['stats']['remote']} / 云端 {r['stats']['cloud']}")
    print(f"  综合检测完备率: {r['avg_detect']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}ms")
    print(f"  三介质: 本地快跨会话丢 / 远程稳慢 / 云端弹性成本")


if __name__ == "__main__":
    main()
