# 文件名: tool_mismatch.py
# 功能: 工具签名与调用方失配+签名校验，止于签名漏校率
# 运行: python tool_mismatch.py

"""工具失配阶：跨版本签名校验，崩在签名漏校。"""

import random

random.seed(42)


def mock_tool_upgrade(version: int, inject_breaking: bool = False) -> dict:
    if inject_breaking:
        return {"version": version, "signature": {"path": str, "mode": str}, "breaking": True}
    return {"version": version, "signature": {"path": str}, "breaking": False}


def validate_signature(caller_sig: dict, tool_sig: dict) -> dict:
    for key in caller_sig:
        if key not in tool_sig:
            return {"matched": False, "reason": f"参数 {key} 失配"}
        if caller_sig[key] != tool_sig[key]:
            return {"matched": False, "reason": f"类型 {key} 失配"}
    return {"matched": True, "reason": "签名适配"}


def simulate_mismatch(n: int = 50) -> dict:
    matched = 0
    mismatched = 0
    for i in range(n):
        tool = mock_tool_upgrade(i, inject_breaking=random.random() < 1.0)
        caller_sig = {"path": str}
        r = validate_signature(caller_sig, tool["signature"])
        if r["matched"]:
            matched += 1
        else:
            mismatched += 1
    return {"matched_rate": matched / n, "mismatched_rate": mismatched / n, "n": n}


def main():
    r = simulate_mismatch(50)
    print("工具失配阶仿真结果（n=50）:")
    print(f"  适配率: {r['matched_rate']:.0%}（签名校验通过）")
    print(f"  失配率: {r['mismatched_rate']:.0%}（Breaking change 致失配）")
    print(f"  崩溃模式: 签名漏校——Breaking change 无校验即崩")


if __name__ == "__main__":
    main()
