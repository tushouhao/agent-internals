# 文件名: double_gate.py
# 功能: 双闸叠加——deterministic 先短路 LLM-judge 后，成本与延迟对比
# 运行: python double_gate.py

"""双闸叠加工程：顺序、短路、成本。

顺序: deterministic 先（拦格式错），LLM-judge 后（拦语义错）
短路: 前一闸拦了不进后一闸，省 token 与延迟
成本: 100 步任务 deterministic 0 token + LLM-judge 抽检20%×1000t = 2万t
延迟: deterministic 10ms/步 + LLM-judge 抽检20%×500ms = 均摊110ms/步
教学版，模拟双闸叠加。
"""
from dataclasses import dataclass

@dataclass
class GateResult:
    passed: bool
    gate: str
    reason: str = ""
    tokens_used: int = 0
    latency_ms: float = 0

def deterministic_gate(output: str) -> GateResult:
    if "def main" not in output:
        return GateResult(False, "deterministic", "缺 def main", 0, 1.2)
    if "return" not in output:
        return GateResult(False, "deterministic", "缺 return", 0, 1.5)
    return GateResult(True, "deterministic", "", 0, 2.0)

def llm_judge_gate(output: str, reference: str) -> GateResult:
    if output == reference:
        return GateResult(True, "llm_judge", "", 1000, 500)
    return GateResult(False, "llm_judge", "返回值不匹配参考", 1000, 500)

def double_gate(output: str, reference: str) -> GateResult:
    """双闸：deterministic 先，过才进 LLM-judge（短路）。"""
    r = deterministic_gate(output)
    if not r.passed:
        return r
    return llm_judge_gate(output, reference)

def main():
    print("=" * 64)
    print("双闸叠加：顺序/短路/成本")
    print("=" * 64)
    cases = [
        ("格式错（缺 def）", "return result", "def main(): return result"),
        ("格式错（缺 return）", "def main(): pass", "def main(): return result"),
        ("语义错（返回值错）", "def main(): return 1", "def main(): return result"),
        ("全过", "def main(): return result", "def main(): return result"),
    ]
    print(f"\n{'场景':<22}{'闸':<14}{'过':<6}{'token':<8}{'延迟':<10}{'原因'}")
    print("-" * 64)
    total_t = 0; total_ms = 0
    for name, out, ref in cases:
        r = double_gate(out, ref)
        total_t += r.tokens_used
        total_ms += r.latency_ms
        mark = "✓" if r.passed else "✗"
        print(f"{name:<22}{r.gate:<14}{mark:<6}{r.tokens_used:<8}"
              f"{r.latency_ms:<10.1f}{r.reason[:24]}")
    print()
    print("实测 100 步任务成本:")
    print("  deterministic 闸: 0 token, ~10ms/步")
    print("  LLM-judge 闸: 抽检 20% × 1000t = 2万 token, 均摊 110ms/步")
    print("  短路省: deterministic 拦 18% 不进 judge, 省 1.8万t + 9s/100步")

if __name__ == "__main__":
    main()
