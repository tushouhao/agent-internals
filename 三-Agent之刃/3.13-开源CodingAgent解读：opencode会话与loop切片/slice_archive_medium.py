# 文件名: slice_archive_medium.py
# 功能: 切片归档介质三策略权衡，止于综合切片完备率
# 运行: python slice_archive_medium.py

"""切片归档介质选择：本地文件 vs 远程数据库 vs 云端。"""

import random

random.seed(42)


def local_file_archive(slice_data: dict) -> dict:
    return {"medium": "local", "latency_ms": 5, "durability": 0.60, "can_replay": random.random() < 0.60}


def remote_db_archive(slice_data: dict) -> dict:
    return {"medium": "remote_db", "latency_ms": 80, "durability": 0.99, "can_replay": random.random() < 0.99}


def cloud_archive(slice_data: dict) -> dict:
    return {"medium": "cloud", "latency_ms": 200, "durability": 0.999, "can_replay": random.random() < 0.999}


def choose_medium(task_criticality: str) -> str:
    if task_criticality == "生死":
        return "cloud"
    if task_criticality == "重要":
        return "remote_db"
    return "local"


def simulate_medium(n: int = 90) -> dict:
    stats = {"local": 0, "remote_db": 0, "cloud": 0}
    replays = []
    latencies = []
    for i in range(n):
        crit = random.choice(["生死", "重要", "普通"])
        medium = choose_medium(crit)
        stats[medium] += 1
        slice_data = {"slice_id": i}
        if medium == "local":
            r = local_file_archive(slice_data)
        elif medium == "remote_db":
            r = remote_db_archive(slice_data)
        else:
            r = cloud_archive(slice_data)
        replays.append(1 if r["can_replay"] else 0)
        latencies.append(r["latency_ms"])
    return {"stats": stats, "n": n, "avg_replay": sum(replays) / len(replays), "avg_latency": sum(latencies) / len(latencies)}


def main():
    """归档介质 demo。"""
    r = simulate_medium(90)
    print("归档介质仿真结果（n=90）:")
    print(f"  分流: 本地 {r['stats']['local']} / 远程 {r['stats']['remote_db']} / 云端 {r['stats']['cloud']}")
    print(f"  综合切片完备率: {r['avg_replay']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}ms")
    print(f"  三介质: 本地快易丢 / 远程稳慢 / 云端弹性成本")


if __name__ == "__main__":
    main()
