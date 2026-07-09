# 文件名: cross_session_resume.py
# 功能: 会话末断点快照 JSON + 新会话首续跑，止于快照失真率
# 运行: python cross_session_resume.py

"""跨会话续阶：断点快照 + 续跑，崩在快照失真。"""

import random
import json
import hashlib

random.seed(42)


def take_snapshot(done_steps: list, react_state: str, todo: list) -> dict:
    """会话末断点快照三件套。"""
    payload = {"done": done_steps, "state": react_state, "todo": todo}
    return {
        "done_steps": done_steps,
        "react_state": react_state,
        "todo": todo,
        "hash": hashlib.md5(json.dumps(payload, ensure_ascii=False).encode()).hexdigest(),
    }


def verify_snapshot(snap: dict) -> bool:
    """校验快照哈希完备性。"""
    payload = {"done": snap.get("done_steps", []), "state": snap.get("react_state", ""), "todo": snap.get("todo", [])}
    expected = hashlib.md5(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
    return expected == snap.get("hash")


def resume_from_snapshot(snap: dict, inject_distortion: bool = False) -> dict:
    """新会话首反序列化续跑。"""
    if inject_distortion:
        snap = dict(snap)
        snap.pop("todo", None)
    if not verify_snapshot(snap):
        return {"resumed": False, "reason": "快照失真"}
    return {"resumed": True, "remaining": len(snap.get("todo", [])), "done": len(snap.get("done_steps", []))}


def simulate_cross_session(n: int = 50) -> dict:
    """跨会话续阶仿真：50 任务续跑率 + 失真率。"""
    resumed = 0
    distortion = 0
    for i in range(n):
        snap = take_snapshot(["步1", "步2"], "推理中", ["步3", "步4"])
        inject = random.random() < 0.22
        r = resume_from_snapshot(snap, inject_distortion=inject)
        if r["resumed"]:
            resumed += 1
        else:
            distortion += 1
    return {"resume_rate": resumed / n, "distortion_rate": distortion / n, "n": n}


def main():
    """跨会话续阶 demo。"""
    r = simulate_cross_session(50)
    print("跨会话续阶仿真结果（n=50）:")
    print(f"  续跑率: {r['resume_rate']:.0%}（断点快照+反序列化）")
    print(f"  快照失真率: {r['distortion_rate']:.0%}（字段遗漏/序列化错）")
    print(f"  崩溃模式: 快照失真——字段遗漏致续跑缺步骤切片漏")


if __name__ == "__main__":
    main()
