# 文件名: depth_limit.py
# 功能: 委托链深度红线 + 三 guard 栈溢出兜底骨架
# 运行: python depth_limit.py

"""深度限: 委托链 depth ≤3 + depth/budget/cycle 三 guard。"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class DelegateChain:
    """委托链状态: depth + 累计 budget + 链上 delegate_id。"""
    depth: int = 0
    cumulative_budget_tokens: int = 0
    budget_limit_tokens: int = 32000
    chain_ids: List[str] = field(default_factory=list)


def check_depth_guard(chain: DelegateChain, new_delegate_id: str, new_budget: int) -> Tuple[bool, str]:
    """depth guard: depth > 3 拒绝再委托。返回 (是否通过, 原因)。"""
    if chain.depth >= 3:
        return False, f"depth guard 拒绝: depth={chain.depth} >= 3，主 Agent 接手"
    return True, f"depth guard 通过: depth={chain.depth} < 3"


def check_budget_guard(chain: DelegateChain, new_budget: int) -> Tuple[bool, str]:
    """budget guard: 累计耗 > 上限 90% 拒绝再委托。"""
    projected = chain.cumulative_budget_tokens + new_budget
    if projected > chain.budget_limit_tokens * 0.9:
        return False, f"budget guard 拒绝: 累计 {projected}t > 上限 {chain.budget_limit_tokens*0.9:.0f}t（90%），降级验收"
    return True, f"budget guard 通过: 累计 {projected}t <= 上限 90%"


def check_cycle_guard(chain: DelegateChain, new_delegate_id: str) -> Tuple[bool, str]:
    """cycle guard: delegate_id 已在链上拒绝（防循环委托死锁）。"""
    if new_delegate_id in chain.chain_ids:
        return False, f"cycle guard 拒绝: {new_delegate_id} 已在链上 {chain.chain_ids}，警报循环"
    return True, f"cycle guard 通过: {new_delegate_id} 不在链上"


def check_all_guards(chain: DelegateChain, new_delegate_id: str, new_budget: int) -> Tuple[bool, str]:
    """三 guard 串联判据（任一不过拒绝）。"""
    for check_name, check_fn in [
        ("depth", lambda: check_depth_guard(chain, new_delegate_id, new_budget)),
        ("budget", lambda: check_budget_guard(chain, new_budget)),
        ("cycle", lambda: check_cycle_guard(chain, new_delegate_id)),
    ]:
        ok, reason = check_fn()
        if not ok:
            return False, f"[{check_name} guard] {reason}"
    return True, "三 guard 全过，允许再委托"


def main():
    """深度红线与三 guard 演示。"""
    print("=== 委托链深度红线 ≤3 层 ===")
    print("主 Agent depth=0 → 子 depth=1 → 孙 depth=2 → 曾孙 depth=3（临界）→ 拒绝再委")

    print("\n=== 三 guard 栈溢出兜底 ===")
    chains = [
        DelegateChain(depth=2, cumulative_budget_tokens=15000, budget_limit_tokens=32000,
                      chain_ids=["del_001", "del_002"]),
        DelegateChain(depth=3, cumulative_budget_tokens=20000, budget_limit_tokens=32000,
                      chain_ids=["del_001", "del_002", "del_003"]),
        DelegateChain(depth=1, cumulative_budget_tokens=29000, budget_limit_tokens=32000,
                      chain_ids=["del_001"]),
        DelegateChain(depth=1, cumulative_budget_tokens=5000, budget_limit_tokens=32000,
                      chain_ids=["del_001", "del_002"]),
    ]
    cases = [
        (chains[0], "del_003", 3000, "场景A 正常再委（depth2 + budget5k + 新ID）"),
        (chains[1], "del_004", 3000, "场景B depth红线临界（depth3）"),
        (chains[2], "del_002", 5000, "场景C budget临界（累计29k + 新5k > 90%）"),
        (chains[3], "del_001", 3000, "场景D cycle循环（del_001 已在链上）"),
    ]

    for chain, new_id, new_budget, label in cases:
        ok, reason = check_all_guards(chain, new_id, new_budget)
        print(f"\n--- {label} ---")
        print(f"  链状态: depth={chain.depth} | 累计{chain.cumulative_budget_tokens}t/{chain.budget_limit_tokens}t | chain={chain.chain_ids}")
        print(f"  拟再委: {new_id} | 新 budget {new_budget}t")
        print(f"  三 guard 判据: {'允许' if ok else '拒绝'}")
        print(f"  原因: {reason}")

    print("\n=== 三 guard 承接关系 ===")
    print("depth guard 防链过深栈帧炸（承接 2.2 7 状态机单流上限）")
    print("budget guard 防链式累爆（承接 2.3 compaction 32k 上限）")
    print("cycle guard 防循环委托死锁（承接 2.9 图式 cycle detection）")
    print("三 guard 串联判据: 任一不过即拒，与 2.14 四红线串联哲学一致")


if __name__ == "__main__":
    main()
