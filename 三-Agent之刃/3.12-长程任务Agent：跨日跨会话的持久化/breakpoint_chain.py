# 文件名: breakpoint_chain.py
# 功能: 跨日多断点链式追溯，止于断点链续跑率
# 运行: python breakpoint_chain.py

"""断点链管理：多日断点链式追溯。"""

import random
import hashlib

random.seed(42)


def make_breakpoint(day: int, steps: list, artifact: str) -> dict:
    """生成单日断点。"""
    return {
        "day": day,
        "steps": steps,
        "artifact": artifact,
        "hash": hashlib.md5(f"{day}:{steps}:{artifact}".encode()).hexdigest(),
    }


def linear_chain(breakpoints: list) -> dict:
    """策略一：线性链顺序追溯。"""
    valid = [bp for bp in breakpoints if bp.get("hash") == hashlib.md5(f"{bp['day']}:{bp['steps']}:{bp['artifact']}".encode()).hexdigest()]
    return {"chain": "linear", "valid_count": len(valid), "total": len(breakpoints), "can_resume": len(valid) == len(breakpoints)}


def branch_merge(breakpoints: list) -> dict:
    """策略二：分支合流。"""
    by_day = {}
    for bp in breakpoints:
        by_day.setdefault(bp["day"], []).append(bp)
    merged = {}
    for day, bps in by_day.items():
        merged[day] = bps[0]
    return {"chain": "branch", "merged_days": len(merged), "can_resume": True}


def fallback_recent(breakpoints: list, fail_idx: int) -> dict:
    """策略三：回退最近有效断点。"""
    for i in range(fail_idx - 1, -1, -1):
        bp = breakpoints[i]
        expected = hashlib.md5(f"{bp['day']}:{bp['steps']}:{bp['artifact']}".encode()).hexdigest()
        if bp.get("hash") == expected:
            return {"chain": "fallback", "resume_from": bp["day"], "can_resume": True}
    return {"chain": "fallback", "can_resume": False}


def simulate_chain(n: int = 30) -> dict:
    """断点链仿真：30 任务多日断点续跑率。"""
    linear_success = 0
    branch_success = 0
    fallback_success = 0
    for i in range(n):
        bps = [make_breakpoint(d, [f"步{d*2+1}", f"步{d*2+2}"], f"产物_{d}") for d in range(1, 4)]
        if linear_chain(bps)["can_resume"]:
            linear_success += 1
        if branch_merge(bps)["can_resume"]:
            branch_success += 1
        if fallback_recent(bps, 3)["can_resume"]:
            fallback_success += 1
    return {
        "n": n,
        "linear_rate": linear_success / n,
        "branch_rate": branch_success / n,
        "fallback_rate": fallback_success / n,
    }


def main():
    """断点链 demo。"""
    r = simulate_chain(30)
    print("断点链仿真结果（n=30）:")
    print(f"  线性链续跑率: {r['linear_rate']:.0%}（顺序追溯逐日校验）")
    print(f"  分支合流续跑率: {r['branch_rate']:.0%}（多分支断点合流）")
    print(f"  回退最近续跑率: {r['fallback_rate']:.0%}（失效断点回退前有效）")
    print(f"  三策略: 线性顺序 / 分支合流 / 回退最近")


if __name__ == "__main__":
    main()
