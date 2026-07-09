# 文件名: scatter_scores.py
# 功能: 卷二 16 篇散点评分回顾 + 收卷困局骨架
# 运行: python scatter_scores.py

"""散点评分回顾: 16 篇每篇给某框架某维度的隐含评分。"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class ScatterScore:
    """散点评分: 出处/框架/维度/暗评分/原因。"""
    source: str
    framework: str
    dimension: str
    score: int
    reason: str


def main():
    """散点评分回顾与收卷困局演示。"""
    scatters = [
        ScatterScore("2.1-2.5", "自研 harness", "可控性", 9,
                    "源码全读 + 状态全透 + 定制无上限"),
        ScatterScore("2.6-2.7", "自研 harness", "生态", 2,
                    "无社区 + 无文档 + 无迭代 + 无绑定"),
        ScatterScore("2.8", "LangChain", "生态", 9,
                    "社区 50k+ stars + 文档全 + 迭代周 + 生态绑定深"),
        ScatterScore("2.9", "LangGraph", "可控性", 7,
                    "状态机显式 + 源码读 + 定制有上限"),
        ScatterScore("2.10", "LlamaIndex", "生态", 8,
                    "社区 30k+ stars + 文档全 + 迭代周"),
        ScatterScore("2.11", "AutoGen", "生态", 7,
                    "社区 15k+ stars + 文档中 + 迭代周"),
        ScatterScore("2.12", "CrewAI", "生态", 6,
                    "社区 8k+ stars + 文档中 + 迭代周"),
        ScatterScore("2.13", "托管", "工程效率", 9,
                    "10-80 行声明 + 厂商调试器"),
        ScatterScore("2.13", "托管", "可控性", 2,
                    "源码闭 + 状态 17% 盲 + 定制绕 Run Steps"),
        ScatterScore("2.14", "MCP 混合", "生态", 6,
                    "协议跨框架 + 社区起步 + 迭代月"),
        ScatterScore("2.14", "MCP 混合", "性能", 7,
                    "本地调用 + 协议损耗 -180ms"),
        ScatterScore("2.15", "决策树", "判据", 10,
                    "收判据未收评分（本篇补）"),
        ScatterScore("2.16", "自研 harness", "可控性", 9,
                    "层级委托纵向扩展 + 序列化契约"),
    ]

    print("=== 卷二 16 篇散点评分回顾 ===")
    print(f"{'出处':8s} | {'框架':14s} | {'维度':8s} | {'暗分':4s} | 依据")
    for s in scatters:
        print(f"{s.source:8s} | {s.framework:14s} | {s.dimension:8s} | {s.score:4d} | {s.reason}")

    print("\n=== 收卷困局: 散评分无横轴对照 ===")
    print("开发者做终极选型要看四维横轴对照:")
    print("  如「LangChain vs LangGraph vs 全自研」生态/效率/可控/性能四维对照")
    print("但散评分:")
    print("  2.8 给 LangChain 生态 9 分，未给 LangGraph/全自研生态分")
    print("  2.13 给托管效率 9 分，未给 LangChain/LangGraph 效率分")
    print("  2.15 决策树收判据（红线串联）未收评分（四维量化）")

    print("\n=== 本篇补刀: 四维评分矩阵 ===")
    print("横轴 7 类框架: LangChain/LangGraph/LlamaIndex/AutoGen/CrewAI/托管/MCP混合/全自研")
    print("纵轴 4 维: 生态成熟度/工程效率/可控性/性能")
    print("每格 0-10 评分，据权重算总评分选最高（第 2 章拆）")


if __name__ == "__main__":
    main()
