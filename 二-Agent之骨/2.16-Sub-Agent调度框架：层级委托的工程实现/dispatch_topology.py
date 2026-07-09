# 文件名: dispatch_topology.py
# 功能: 串行/并行/树状三种委托拓扑延迟与合并骨架
# 运行: python dispatch_topology.py

"""调度策略: 串行/并行/树状三拓扑延迟模型与结果合并。"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class SubAgentRun:
    """子 Agent 单次执行画像。"""
    name: str
    seconds: float
    result: Dict[str, object]


def serial_delay(runs: List[SubAgentRun]) -> float:
    """串行拓扑延迟: 累加 Σ 子 Agent 时间。"""
    return sum(r.seconds for r in runs)


def parallel_delay(runs: List[SubAgentRun]) -> float:
    """并行拓扑延迟: 取 max 子 Agent 时间。"""
    return max(r.seconds for r in runs) if runs else 0.0


def tree_delay(layers: List[List[SubAgentRun]]) -> float:
    """树状拓扑延迟: 层内并行 max + 层间串行累加。"""
    return sum(parallel_delay(layer) for layer in layers)


def serial_merge(runs: List[SubAgentRun]) -> Dict:
    """串行合并: 结果链（后子 Agent 可读前子 Agent 结果）。"""
    chain = {}
    for r in runs:
        chain[r.name] = r.result
    return {"type": "serial_chain", "chain": chain}


def parallel_merge(runs: List[SubAgentRun]) -> Dict:
    """并行合并: 结果集（子 Agent 间无依赖，结果并列）。"""
    return {"type": "parallel_set", "set": {r.name: r.result for r in runs}}


def tree_merge(layers: List[List[SubAgentRun]]) -> Dict:
    """树状合并: 层层合并（层内并行集 + 层间串行链）。"""
    merged_layers = []
    for layer in layers:
        merged_layers.append({r.name: r.result for r in layer})
    return {"type": "tree", "layers": merged_layers}


def main():
    """三拓扑延迟与合并演示。"""
    runs = [
        SubAgentRun("子A", 30, {"price": 99}),
        SubAgentRun("子B", 50, {"price": 88}),
        SubAgentRun("子C", 40, {"price": 77}),
    ]

    print("=== 串行拓扑 ===")
    print(f"延迟: {serial_delay(runs)}s（累加 Σ 30+50+40）")
    print(f"顺序保证: 强（先后依赖，子B 可读子A 结果）")
    print(f"合并: {serial_merge(runs)}")

    print("\n=== 并行拓扑 ===")
    print(f"延迟: {parallel_delay(runs)}s（取 max 50）")
    print(f"顺序保证: 无（并发完成，子 Agent 间无依赖）")
    print(f"合并: {parallel_merge(runs)}")

    print("\n=== 树状拓扑 ===")
    layers = [
        [SubAgentRun("子A", 30, {"step": "抓取"})],
        [SubAgentRun("子A1", 20, {"step": "解析"}), SubAgentRun("子A2", 25, {"step": "校验"})],
        [SubAgentRun("子B", 15, {"step": "汇总"})],
    ]
    print(f"延迟: {tree_delay(layers)}s（层内 max + 层间累加 = 30+25+15）")
    print(f"顺序保证: 局部强（层内无依赖，层间有依赖）")
    print(f"合并: {tree_merge(layers)}")

    print("\n=== 三拓扑对照 ===")
    print(f"{'拓扑':6s} | {'延迟':20s} | {'顺序':16s} | {'合并':12s} | 适用")
    print(f"{'串行':6s} | {'累加 Σ':20s} | {'强（先后依赖）':16s} | {'结果链':12s} | 子任务有依赖")
    print(f"{'并行':6s} | {'取 max':20s} | {'无（并发）':16s} | {'结果集':12s} | 子任务独立")
    print(f"{'树状':6s} | {'分层 max 累加':20s} | {'局部强（层内）':16s} | {'层层合并':12s} | 子任务再拆")

    print("\n=== 承接 2.9 图式分支并行 ===")
    print("并行拓扑与 2.9 LangGraph 分支并行思路同构:")
    print("  2.9: 并行节点取 max 延迟 + 结果合并（单 Agent 内）")
    print("  本篇: 并行拓扑取 max 延迟 + 结果集合并（多 Agent 间）")
    print("树状拓扑是串行+并行复合，适合深度委托场景")


if __name__ == "__main__":
    main()
