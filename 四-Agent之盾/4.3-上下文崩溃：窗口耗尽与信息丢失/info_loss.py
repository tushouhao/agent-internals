# 文件名: info_loss.py
# 功能: 长上下文关键信息截断丢失+关键性检测，止于关键漏检率
# 运行: python info_loss.py

"""信息丢失阶：长上下文关键检测，崩在关键漏检。"""

import random

random.seed(42)


def mock_long_context_truncate(ctx_len: int, inject_loss: bool = False) -> dict:
    if inject_loss:
        return {"ctx_len": ctx_len, "key_info": "", "lost": True}
    return {"ctx_len": ctx_len, "key_info": "关键参数", "lost": False}


def detect_key_info(ctx: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"loss_detected": False, "missed": True}
    return {"loss_detected": ctx["key_info"] == "", "missed": False}


def simulate_loss(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        ctx = mock_long_context_truncate(i, inject_loss=random.random() < 0.94)
        r = detect_key_info(ctx, inject_miss=random.random() < 0.06)
        if r["loss_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_loss(50)
    print("信息丢失阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（关键丢失被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（关键性检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致信息丢失残留）")
    print(f"  崩溃模式: 关键漏检——关键性检测漏检致信息丢失无从防患")


if __name__ == "__main__":
    main()
