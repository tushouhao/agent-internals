# 文件名: skill_registry_medium.py
# 功能: skill 注册表介质三策略权衡，止于综合复用率
# 运行: python skill_registry_medium.py

"""skill 注册表介质选择：本地内存 vs 远程注册中心 vs 云端共享。"""

import random

random.seed(42)


def local_memory_registry(skill_data: dict) -> dict:
    return {"medium": "local", "latency_ms": 1, "reuse": 0.50, "can_reuse": random.random() < 0.50}


def remote_registry_center(skill_data: dict) -> dict:
    return {"medium": "remote", "latency_ms": 30, "reuse": 0.95, "can_reuse": random.random() < 0.95}


def cloud_shared_registry(skill_data: dict) -> dict:
    return {"medium": "cloud", "latency_ms": 80, "reuse": 0.99, "can_reuse": random.random() < 0.99}


def choose_medium(task_scope: str) -> str:
    if task_scope == "跨会话":
        return "cloud"
    if task_scope == "跨进程":
        return "remote"
    return "local"


def simulate_medium(n: int = 90) -> dict:
    """注册表介质仿真：90 任务综合复用率。"""
    stats = {"local": 0, "remote": 0, "cloud": 0}
    reuses = []
    latencies = []
    for i in range(n):
        scope = random.choice(["跨会话", "跨进程", "单会话"])
        medium = choose_medium(scope)
        stats[medium] += 1
        skill_data = {"skill_id": i}
        if medium == "local":
            r = local_memory_registry(skill_data)
        elif medium == "remote":
            r = remote_registry_center(skill_data)
        else:
            r = cloud_shared_registry(skill_data)
        reuses.append(1 if r["can_reuse"] else 0)
        latencies.append(r["latency_ms"])
    return {"stats": stats, "n": n, "avg_reuse": sum(reuses) / len(reuses), "avg_latency": sum(latencies) / len(latencies)}


def main():
    """注册表介质 demo。"""
    r = simulate_medium(90)
    print("注册表介质仿真结果（n=90）:")
    print(f"  分流: 本地 {r['stats']['local']} / 远程 {r['stats']['remote']} / 云端 {r['stats']['cloud']}")
    print(f"  综合复用率: {r['avg_reuse']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}ms")
    print(f"  三介质: 本地快跨会话丢 / 远程稳慢 / 云端弹性成本")


if __name__ == "__main__":
    main()
