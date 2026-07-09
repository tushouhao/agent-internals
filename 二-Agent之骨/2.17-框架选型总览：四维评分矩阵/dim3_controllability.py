# 文件名: dim3_controllability.py
# 功能: 维三可控性三子项评分骨架
# 运行: python dim3_controllability.py

"""维三可控性: 源码可读/状态透明/定制深度三子项加权。"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class FrameworkControllability:
    """框架可控性画像: 三子项分。"""
    name: str
    source_readable: int
    state_transparent: int
    customization_depth: int


def controllability_total(f: FrameworkControllability, weights: Tuple[float, float, float]) -> float:
    """可控总分 = 源码*0.3 + 状态*0.4 + 定制*0.3。"""
    return (f.source_readable * weights[0] + f.state_transparent * weights[1]
            + f.customization_depth * weights[2])


def main():
    """维三可控性评分演示。"""
    frameworks = [
        FrameworkControllability("LangChain", 8, 5, 5),
        FrameworkControllability("LangGraph", 8, 7, 7),
        FrameworkControllability("LlamaIndex", 8, 6, 6),
        FrameworkControllability("AutoGen", 8, 7, 7),
        FrameworkControllability("CrewAI", 8, 6, 6),
        FrameworkControllability("托管", 2, 2, 2),
        FrameworkControllability("MCP混合", 6, 6, 6),
        FrameworkControllability("全自研", 10, 9, 9),
    ]
    weights = (0.3, 0.4, 0.3)

    print("=== 维三可控性三子项评分 ===")
    print(f"{'框架':10s} | {'源码0.3':8s} | {'状态0.4':8s} | {'定制0.3':8s} | 总分")
    for f in frameworks:
        total = controllability_total(f, weights)
        print(f"{f.name:10s} | {f.source_readable:8d} | {f.state_transparent:8d} | {f.customization_depth:8d} | {total:.1f}")

    print("\n=== 可控总分排名 ===")
    ranked = [(f.name, controllability_total(f, weights)) for f in frameworks]
    ranked.sort(key=lambda x: x[1], reverse=True)
    for i, (name, total) in enumerate(ranked, 1):
        print(f"  {i}. {name}: {total:.1f}")

    print("\n=== 承接卷二散点评分 ===")
    print("2.1-2.5 自研可控 9 暗评 → 本篇显式量化 9.3（源码10+状态9+定制9 加权）")
    print("2.13 托管可控 2 暗评 → 本篇显式量化 2.0（源码2+状态2+定制2 加权）")
    print("2.9 LangGraph 可控 7 暗评 → 本篇显式量化 7.0（源码8+状态7+定制7 加权）")
    print("洞察: 全自研可控满分承接 2.16 序列化契约（主→子全可控）")
    print("洞察: 托管可控 2 分承接 2.13 四崩点（源码闭/状态盲/定制绕）")
    print("洞察: 框架内源码读均 8 分（开源），但状态/定制差在框架设计")


if __name__ == "__main__":
    main()
