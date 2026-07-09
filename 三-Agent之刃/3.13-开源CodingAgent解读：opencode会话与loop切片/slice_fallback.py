# 文件名: slice_fallback.py
# 功能: 切片缺失降级兜底三策略，止于切片完备率
# 运行: python slice_fallback.py

"""切片缺失降级兜底：从剩余切片反推缺失维。"""

import random

random.seed(42)


def mock_loop_trace(steps: int) -> list:
    return [{"step": s, "action": f"行动{s}", "observe": f"观察{s}"} for s in range(steps)]


def reconstruct_artifact_from_loop(loop: list) -> str:
    if not loop:
        return ""
    return loop[-1].get("observe", "")


def reconstruct_loop_from_artifact(artifact: str) -> list:
    return [{"step": 0, "action": "未知", "observe": artifact}]


def reconstruct_session_from_loop_art(loop: list, art: str) -> dict:
    return {"session_id": -1, "reconstructed": True, "loop_steps": len(loop), "artifact": art}


def simulate_fallback(n: int = 30) -> dict:
    success = 0
    for i in range(n):
        loop = mock_loop_trace(3)
        art = f"产物_{i}"
        missing = random.choice(["artifact", "loop", "session"])
        if missing == "artifact":
            rec = reconstruct_artifact_from_loop(loop)
            if rec:
                success += 1
        elif missing == "loop":
            rec = reconstruct_loop_from_artifact(art)
            if rec:
                success += 1
        else:
            rec = reconstruct_session_from_loop_art(loop, art)
            if rec:
                success += 1
    return {"n": n, "fallback_success_rate": success / n}


def main():
    """降级兜底 demo。"""
    r = simulate_fallback(30)
    print("降级兜底仿真结果（n=30）:")
    print(f"  兜底成功率: {r['fallback_success_rate']:.0%}（从剩余切片反推缺失维）")
    print(f"  三策略: 产物缺 loop 反推 / loop 缺产物反推 / 会话缺 loop+产物反推")


if __name__ == "__main__":
    main()
