# 文件名: skill_conflict_fallback.py
# 功能: 注册冲突降级兜底三策略，止于 skill 复用率
# 运行: python skill_conflict_fallback.py

"""注册冲突降级兜底：从兼容/重建/回退保 skill 复用率。"""

import random

random.seed(42)


def compat_old_signature(new_sig: dict, old_sig: dict) -> dict:
    """策略一：旧签名兼容（参数增默认值/类型转）。"""
    compat = {}
    for k, v in old_sig.items():
        if k in new_sig:
            compat[k] = new_sig[k]
        else:
            compat[k] = v
    return {"compatible": True, "sig": compat}


def rebuild_skill(new_sig: dict, old_name: str) -> dict:
    """策略二：重建 skill（新名注册避免冲突）。"""
    return {"compatible": False, "rebuilt": True, "new_name": f"{old_name}_v2", "sig": new_sig}


def fallback_to_multi_agent() -> dict:
    """策略三：回退多 Agent（放弃复用走委托）。"""
    return {"compatible": False, "rebuilt": False, "fallback": "multi_agent"}


def simulate_fallback(n: int = 30) -> dict:
    """降级兜底仿真：30 冲突复用率。"""
    success = 0
    for i in range(n):
        conflict_type = random.choice(["签名变", "不可兼容", "handler 失配"])
        if conflict_type == "签名变":
            r = compat_old_signature({"param": f"新_{i}"}, {"param": "旧", "extra": "默认"})
            if r["compatible"]:
                success += 1
        elif conflict_type == "不可兼容":
            r = rebuild_skill({"param": f"新_{i}"}, f"skill_{i}")
            if r["rebuilt"]:
                success += 1
        else:
            r = fallback_to_multi_agent()
            if r["fallback"]:
                success += 1
    return {"n": n, "fallback_success_rate": success / n}


def main():
    """降级兜底 demo。"""
    r = simulate_fallback(30)
    print("降级兜底仿真结果（n=30）:")
    print(f"  兜底成功率: {r['fallback_success_rate']:.0%}（兼容/重建/回退三策略）")
    print(f"  三策略: 签名变兼容 / 不可兼容重建 / handler 失配回退多 Agent")


if __name__ == "__main__":
    main()
