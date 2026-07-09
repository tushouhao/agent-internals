# 文件名: full_slice_archive.py
# 功能: 会话/loop/产物三维切片归档哈希索引，止于切片缺失率
# 运行: python full_slice_archive.py

"""全切片阶：三维切片归档，崩在切片缺失。"""

import random
import hashlib
import json

random.seed(42)


def archive_slice(session_meta: dict, loop_trace: list, artifact: str) -> dict:
    """三维切片归档 + 哈希索引。"""
    h_session = hashlib.md5(json.dumps(session_meta, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    h_loop = hashlib.md5(json.dumps(loop_trace, ensure_ascii=False).encode()).hexdigest()
    h_art = hashlib.md5(artifact.encode()).hexdigest()
    return {
        "session": session_meta,
        "loop": loop_trace,
        "artifact": artifact,
        "hash_session": h_session,
        "hash_loop": h_loop,
        "hash_art": h_art,
    }


def verify_slice(archived: dict) -> dict:
    """校验三维切片完备性。"""
    missing = []
    if not archived.get("hash_session"):
        missing.append("会话切片")
    if not archived.get("hash_loop"):
        missing.append("loop 切片")
    if not archived.get("hash_art"):
        missing.append("产物切片")
    return {"complete": len(missing) == 0, "missing": missing}


def simulate_full_slice(n: int = 50) -> dict:
    """全切片阶仿真：50 任务切片完备率 + 缺失率。"""
    complete = 0
    missing_total = 0
    for i in range(n):
        meta = {"session_id": i, "task": f"任务_{i}", "timestamp": "2026-07-08T22:00Z"}
        trace = [{"step": s, "thought": f"推理{s}", "action": f"行动{s}"} for s in range(3)]
        art = f"产物_{i}"
        archived = archive_slice(meta, trace, art)
        if random.random() < 0.15:
            dim = random.choice(["hash_session", "hash_loop", "hash_art"])
            archived[dim] = ""
        v = verify_slice(archived)
        if v["complete"]:
            complete += 1
        else:
            missing_total += 1
    return {"complete_rate": complete / n, "missing_rate": missing_total / n, "n": n}


def main():
    """全切片阶 demo。"""
    r = simulate_full_slice(50)
    print("全切片阶仿真结果（n=50）:")
    print(f"  切片完备率: {r['complete_rate']:.0%}（三维哈希齐全）")
    print(f"  切片缺失率: {r['missing_rate']:.0%}（任一维遗漏）")
    print(f"  崩溃模式: 切片缺失——维度遗漏致复盘不可回溯")


if __name__ == "__main__":
    main()
