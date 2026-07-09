# 文件名: cycle_detect_medium.py
# 功能: 环检测存储介质三策略权衡，止于综合检测完备率
# 运行: python cycle_detect_medium.py

"""环检测存储介质选择：本地内存 vs 远程图数据库 vs 云端图服务。"""

import random

random.seed(42)


def local_memory_graph(graph_data: dict) -> dict:
    return {"medium": "local", "latency_ms": 1, "durability": 0.50, "can_detect": random.random() < 0.50}


def remote_graph_db(graph_data: dict) -> dict:
    return {"medium": "remote", "latency_ms": 50, "durability": 0.99, "can_detect": random.random() < 0.99}


def cloud_graph_service(graph_data: dict) -> dict:
    return {"medium": "cloud", "latency_ms": 150, "durability": 0.999, "can_detect": random.random() < 0.999}


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
        graph_data = {"graph_id": i}
        if medium == "local":
            r = local_memory_graph(graph_data)
        elif medium == "remote":
            r = remote_graph_db(graph_data)
        else:
            r = cloud_graph_service(graph_data)
        detects.append(1 if r["can_detect"] else 0)
        latencies.append(r["latency_ms"])
    return {"stats": stats, "n": n, "avg_detect": sum(detects) / len(detects), "avg_latency": sum(latencies) / len(latencies)}


def main():
    r = simulate_medium(90)
    print("环检测介质仿真结果（n=90）:")
    print(f"  分流: 本地 {r['stats']['local']} / 远程 {r['stats']['remote']} / 云端 {r['stats']['cloud']}")
    print(f"  综合检测完备率: {r['avg_detect']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}ms")
    print(f"  三介质: 本地快跨会话丢 / 远程稳慢 / 云端弹性成本")


if __name__ == "__main__":
    main()
