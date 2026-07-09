# 文件名: dim2_efficiency.py
# 功能: 维二工程效率三子项评分骨架
# 运行: python dim2_efficiency.py

"""维二工程效率: 上手成本/配置量/调试便利三子项加权。"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class FrameworkEfficiency:
    """框架效率画像: 三子项分。"""
    name: str
    learn_cost: int
    config_loc: int
    debug_convenience: int


def efficiency_total(f: FrameworkEfficiency, weights: Tuple[float, float, float]) -> float:
    """效率总分 = 上手*0.4 + 配置*0.4 + 调试*0.2。"""
    return (f.learn_cost * weights[0] + f.config_loc * weights[1]
            + f.debug_convenience * weights[2])


def main():
    """维二工程效率评分演示。"""
    frameworks = [
        FrameworkEfficiency("LangChain", 7, 7, 7),
        FrameworkEfficiency("LangGraph", 6, 6, 7),
        FrameworkEfficiency("LlamaIndex", 7, 7, 7),
        FrameworkEfficiency("AutoGen", 6, 6, 6),
        FrameworkEfficiency("CrewAI", 7, 7, 6),
        FrameworkEfficiency("托管", 9, 9, 8),
        FrameworkEfficiency("MCP混合", 5, 5, 6),
        FrameworkEfficiency("全自研", 3, 3, 9),
    ]
    weights = (0.4, 0.4, 0.2)

    print("=== 维二工程效率三子项评分 ===")
    print(f"{'框架':10s} | {'上手0.4':8s} | {'配置0.4':8s} | {'调试0.2':8s} | 总分")
    for f in frameworks:
        total = efficiency_total(f, weights)
        print(f"{f.name:10s} | {f.learn_cost:8d} | {f.config_loc:8d} | {f.debug_convenience:8d} | {total:.1f}")

    print("\n=== 效率总分排名 ===")
    ranked = [(f.name, efficiency_total(f, weights)) for f in frameworks]
    ranked.sort(key=lambda x: x[1], reverse=True)
    for i, (name, total) in enumerate(ranked, 1):
        print(f"  {i}. {name}: {total:.1f}")

    print("\n=== 承接卷二散点评分 ===")
    print("2.13 托管效率 9 暗评 → 本篇显式量化 8.8（上手9+配置9+调试8 加权）")
    print("2.1 自研效率 3 暗评 → 本篇显式量化 3.6（上手3+配置3+调试9 加权）")
    print("洞察: 托管效率最高但调试 8 非满分（厂商调试器有盲区 17% 承接 2.13）")
    print("洞察: 全自研调试 9 满分（自调试全可控）但上手/配置低拉低总分")


if __name__ == "__main__":
    main()
