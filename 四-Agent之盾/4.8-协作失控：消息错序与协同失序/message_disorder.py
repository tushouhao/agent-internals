# 文件名: message_disorder.py
# 功能: 多 Agent 消息顺序错乱止于检测缺失致错序率 100%
# 运行: python message_disorder.py

"""消息错序阶：消息顺序错乱，崩在检测漏。"""

import random

random.seed(42)


def mock_message_disorder(msg_id: int, inject_disorder: bool = False) -> dict:
    if inject_disorder:
        return {"id": msg_id, "seq": msg_id + 5, "expected": msg_id, "disordered": True}
    return {"id": msg_id, "seq": msg_id, "expected": msg_id, "disordered": False}


def detect_disorder(seq: int, expected: int) -> bool:
    return seq == expected


def run_message_disorder(msg_id: int) -> dict:
    r = mock_message_disorder(msg_id, inject_disorder=random.random() < 1.0)
    if detect_disorder(r["seq"], r["expected"]):
        return {"delivered": True, "reason": "顺序正确", "disordered": False}
    return {"delivered": False, "reason": "消息错序", "disordered": True}


def simulate_disorder(n: int = 50) -> dict:
    delivered = 0
    disordered = 0
    for i in range(n):
        r = run_message_disorder(i)
        if r["delivered"]:
            delivered += 1
        else:
            disordered += 1
    return {"delivered_rate": delivered / n, "disordered_rate": disordered / n, "n": n}


def main():
    r = simulate_disorder(50)
    print("消息错序阶仿真结果（n=50）:")
    print(f"  送达率: {r['delivered_rate']:.0%}（顺序正确即送达）")
    print(f"  错序率: {r['disordered_rate']:.0%}（消息序号偏离预期）")
    print(f"  崩溃模式: 检测漏——消息错序无检测即弃无从防患")


if __name__ == "__main__":
    main()
