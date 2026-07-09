# 文件名: cross_day_persist.py
# 功能: 断点冷存 + 一致性哈希校验 + 过夜续跑，止于漂移率
# 运行: python cross_day_persist.py

"""跨日阶：冷存 + 一致性校验，崩在状态漂移。"""

import random
import hashlib

random.seed(42)


def cold_store(artifact: str, deps: list, env: dict) -> dict:
    """断点冷存：产物 + 依赖 + 环境 三哈希。"""
    return {
        "artifact": artifact,
        "deps": deps,
        "env": env,
        "hash_art": hashlib.md5(artifact.encode()).hexdigest(),
        "hash_deps": hashlib.md5("|".join(deps).encode()).hexdigest(),
        "hash_env": hashlib.md5(str(sorted(env.items())).encode()).hexdigest(),
    }


def verify_consistency(stored: dict, current_art: str, current_deps: list, current_env: dict) -> dict:
    """过夜续跑首比对三哈希。"""
    drift = []
    if hashlib.md5(current_art.encode()).hexdigest() != stored["hash_art"]:
        drift.append("产物漂移")
    if hashlib.md5("|".join(current_deps).encode()).hexdigest() != stored["hash_deps"]:
        drift.append("依赖漂移")
    if hashlib.md5(str(sorted(current_env.items())).encode()).hexdigest() != stored["hash_env"]:
        drift.append("环境漂移")
    return {"consistent": len(drift) == 0, "drift": drift}


def resume_cross_day(stored: dict, inject_drift: bool = False) -> dict:
    """过夜续跑 + 一致性校验。"""
    if inject_drift:
        current_deps = stored["deps"] + ["新依赖_过夜引入"]
    else:
        current_deps = stored["deps"]
    v = verify_consistency(stored, stored["artifact"], current_deps, stored["env"])
    if v["consistent"]:
        return {"resumed": True, "drift": []}
    if "产物漂移" in v["drift"]:
        return {"resumed": True, "action": "重算产物", "drift": v["drift"]}
    if "依赖漂移" in v["drift"]:
        return {"resumed": True, "action": "降级兼容", "drift": v["drift"]}
    return {"resumed": True, "action": "回退版本", "drift": v["drift"]}


def simulate_cross_day(n: int = 50) -> dict:
    """跨日阶仿真：50 任务漂移率 + 续跑率。"""
    resumed = 0
    drift_total = 0
    for i in range(n):
        stored = cold_store(f"产物_{i}", ["dep_a==1.0", "dep_b==2.0"], {"python": "3.11"})
        inject = random.random() < 0.07
        r = resume_cross_day(stored, inject_drift=inject)
        if r["resumed"]:
            resumed += 1
        if r.get("drift"):
            drift_total += 1
    return {
        "resume_rate": resumed / n,
        "drift_rate": drift_total / n,
        "n": n,
    }


def main():
    """跨日阶 demo。"""
    r = simulate_cross_day(50)
    print("跨日阶仿真结果（n=50）:")
    print(f"  续跑率: {r['resume_rate']:.0%}（冷存+一致性校验+漂移应对）")
    print(f"  漂移率: {r['drift_rate']:.0%}（产物/依赖/环境 漂移）")
    print(f"  崩溃模式: 状态漂移——过夜后依赖版本变致中间产物失效")
    print(f"  三应对: 产物漂移重算 / 依赖漂移降级兼容 / 环境漂移回退版本")


if __name__ == "__main__":
    main()
