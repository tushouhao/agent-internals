# 文件名: skill_registry.py
# 功能: skill 动态注册+热加载+跨会话复用，止于注册冲突率
# 运行: python skill_registry.py

"""skill 注册阶：动态注册+热加载+复用，崩在注册冲突。"""

import random
import hashlib
import json

random.seed(42)


def register_skill(name: str, signature: dict, handler: str) -> dict:
    """skill 动态注册三件套（名+签名+实现）。"""
    payload = {"name": name, "signature": signature, "handler": handler}
    return {
        "name": name,
        "signature": signature,
        "handler": handler,
        "hash": hashlib.md5(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "loaded": True,
    }


def hot_reload_skill(registry: dict, new_skill: dict) -> dict:
    """热加载 skill（同名覆盖 + 签名变冲突）。"""
    name = new_skill["name"]
    if name in registry:
        old_sig = registry[name]["signature"]
        if old_sig != new_skill["signature"]:
            return {"reloaded": False, "reason": "签名冲突", "conflict": True}
    registry[name] = new_skill
    return {"reloaded": True, "conflict": False}


def simulate_skill_registry(n: int = 50) -> dict:
    """skill 注册阶仿真：50 注册冲突率 + 复用率。"""
    registry = {}
    conflict = 0
    reused = 0
    for i in range(n):
        if random.random() < 0.30 and registry:
            name = random.choice(list(registry.keys()))
            sig = {"param": f"新参数_{i}"}
        else:
            name = f"skill_{i}"
            sig = {"param": f"参数_{i}"}
        skill = register_skill(name, sig, f"handler_{i}")
        r = hot_reload_skill(registry, skill)
        if r["conflict"]:
            conflict += 1
        else:
            reused += 1
    return {"conflict_rate": conflict / n, "reuse_rate": reused / n, "registry_size": len(registry), "n": n}


def main():
    """skill 注册阶 demo。"""
    r = simulate_skill_registry(50)
    print("skill 注册阶仿真结果（n=50）:")
    print(f"  注册冲突率: {r['conflict_rate']:.0%}（同名+签名变）")
    print(f"  复用率: {r['reuse_rate']:.0%}（动态注册+热加载）")
    print(f"  注册表大小: {r['registry_size']}（去重后）")
    print(f"  崩溃模式: 注册冲突——同名/签名变致热加载失败")


if __name__ == "__main__":
    main()
