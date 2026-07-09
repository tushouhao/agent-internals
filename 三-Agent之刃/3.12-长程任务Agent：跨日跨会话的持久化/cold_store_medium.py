# 文件名: cold_store_medium.py
# 功能: 断点冷存介质三策略权衡，止于综合续跑率
# 运行: python cold_store_medium.py

"""冷存介质选择：本地文件 vs 远程数据库 vs 云端。"""

import random

random.seed(42)


def local_file_store(snap: dict) -> dict:
    """本地文件：快但易丢。"""
    return {"medium": "local", "latency_ms": 5, "durability": 0.60, "can_resume": random.random() < 0.60}


def remote_db_store(snap: dict) -> dict:
    """远程数据库：稳但慢。"""
    return {"medium": "remote_db", "latency_ms": 80, "durability": 0.99, "can_resume": random.random() < 0.99}


def cloud_store(snap: dict) -> dict:
    """云端：弹性但成本。"""
    return {"medium": "cloud", "latency_ms": 200, "durability": 0.999, "can_resume": random.random() < 0.999}


def choose_medium(task_criticality: str) -> str:
    """按任务关键性选介质。"""
    if task_criticality == "生死":
        return "cloud"
    if task_criticality == "重要":
        return "remote_db"
    return "local"


def simulate_medium(n: int = 90) -> dict:
    """冷存介质仿真：90 任务综合续跑率。"""
    stats = {"local": 0, "remote_db": 0, "cloud": 0}
    resumes = []
    latencies = []
    for i in range(n):
        crit = random.choice(["生死", "重要", "普通"])
        medium = choose_medium(crit)
        stats[medium] += 1
        snap = {"artifact": f"产物_{i}"}
        if medium == "local":
            r = local_file_store(snap)
        elif medium == "remote_db":
            r = remote_db_store(snap)
        else:
            r = cloud_store(snap)
        resumes.append(1 if r["can_resume"] else 0)
        latencies.append(r["latency_ms"])
    return {
        "stats": stats,
        "n": n,
        "avg_resume": sum(resumes) / len(resumes),
        "avg_latency": sum(latencies) / len(latencies),
    }


def main():
    """冷存介质 demo。"""
    r = simulate_medium(90)
    print("冷存介质仿真结果（n=90）:")
    print(f"  分流: 本地 {r['stats']['local']} / 远程 {r['stats']['remote_db']} / 云端 {r['stats']['cloud']}")
    print(f"  综合续跑率: {r['avg_resume']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}ms")
    print(f"  三介质: 本地快易丢 / 远程稳慢 / 云端弹性成本")


if __name__ == "__main__":
    main()
