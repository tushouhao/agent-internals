# 文件名: matrix_skeleton.py
# 功能: 四维评分矩阵骨架 + 7×4 网格评分骨架
# 运行: python matrix_skeleton.py

"""四维评分矩阵: 横轴 7 类框架 × 纬轴 4 维度，每格 0-10 评分。"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class MatrixCell:
    """矩阵格: 框架/维度/评分/依据。"""
    framework: str
    dimension: str
    score: int
    basis: str


@dataclass
class ScoreMatrix:
    """评分矩阵: 横轴框架清单 + 纬轴维度清单 + 格评分。"""
    frameworks: List[str] = field(default_factory=list)
    dimensions: List[str] = field(default_factory=list)
    cells: Dict[Tuple[str, str], MatrixCell] = field(default_factory=dict)

    def add_cell(self, cell: MatrixCell) -> None:
        self.cells[(cell.framework, cell.dimension)] = cell

    def get_score(self, framework: str, dimension: str) -> int:
        cell = self.cells.get((framework, dimension))
        return cell.score if cell else 0

    def total_score(self, framework: str, weights: Dict[str, float]) -> float:
        """据四维权重算框架总评分（加权平均）。"""
        total = 0.0
        for dim, weight in weights.items():
            total += self.get_score(framework, dim) * weight
        return total

    def recommend(self, weights: Dict[str, float]) -> Tuple[str, float, List[Tuple[str, float]]]:
        """据权重推荐最高分框架。返回 (框架, 总分, 全框架排名)。"""
        rankings = [(fw, self.total_score(fw, weights)) for fw in self.frameworks]
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings[0][0], rankings[0][1], rankings


def build_matrix() -> ScoreMatrix:
    """建四维评分矩阵（承接散点评分显式量化）。"""
    matrix = ScoreMatrix(
        frameworks=["LangChain", "LangGraph", "LlamaIndex", "AutoGen", "CrewAI",
                    "托管", "MCP混合", "全自研"],
        dimensions=["生态成熟度", "工程效率", "可控性", "性能"])
    for fw, s, b in [("LangChain", 9, "50k+ stars/文档全/迭代周"), ("LangGraph", 7, "15k+ stars/文档全/迭代周"),
                      ("LlamaIndex", 8, "30k+ stars/文档全/迭代周"), ("AutoGen", 7, "15k+ stars/文档中/迭代周"),
                      ("CrewAI", 6, "8k+ stars/文档中/迭代周"), ("托管", 8, "厂商全/文档全/但闭源"),
                      ("MCP混合", 6, "协议跨框架/社区起步/迭代月"), ("全自研", 2, "无社区/无文档/无迭代/无绑定")]:
        matrix.add_cell(MatrixCell(fw, "生态成熟度", s, b))
    for fw, s, b in [("LangChain", 7, "80-160 行配置/上手 2 周"), ("LangGraph", 6, "120-200 行/上手 3 周"),
                      ("LlamaIndex", 7, "100-180 行/上手 2 周"), ("AutoGen", 6, "100-200 行/上手 3 周"),
                      ("CrewAI", 7, "80-180 行/上手 2 周"), ("托管", 9, "10-80 行声明/厂商调试器"),
                      ("MCP混合", 5, "180 行配置/上手 4 周"), ("全自研", 3, "280-450 行/自调试")]:
        matrix.add_cell(MatrixCell(fw, "工程效率", s, b))
    for fw, s, b in [("LangChain", 5, "源码读/状态半透/定制有上限"), ("LangGraph", 7, "状态机显式/源码读/定制有上限"),
                      ("LlamaIndex", 6, "源码读/状态半透/定制有上限"), ("AutoGen", 7, "源码读/状态显式/定制有上限"),
                      ("CrewAI", 6, "源码读/状态半透/定制有上限"), ("托管", 2, "源码闭/状态17%盲/定制绕Run Steps"),
                      ("MCP混合", 6, "协议透/状态半透/定制协议限"), ("全自研", 9, "源码全读/状态全透/定制无上限")]:
        matrix.add_cell(MatrixCell(fw, "可控性", s, b))
    for fw, s, b in [("LangChain", 6, "延迟中/吞吐中/资源中"), ("LangGraph", 6, "延迟中/吞吐中/资源中"),
                      ("LlamaIndex", 7, "延迟低/吞吐高/资源低（检索优化）"), ("AutoGen", 5, "延迟高/吞吐低/资源高（多角色）"),
                      ("CrewAI", 5, "延迟高/吞吐低/资源高（多角色）"), ("托管", 5, "网络延迟/Runs 2.3x/资源低"),
                      ("MCP混合", 7, "本地调用/协议损耗 -180ms/资源中"), ("全自研", 8, "延迟低/吞吐高/资源可控")]:
        matrix.add_cell(MatrixCell(fw, "性能", s, b))
    return matrix


def main():
    """矩阵骨架与推荐演示。"""
    matrix = build_matrix()

    print("=== 四维评分矩阵骨架 ===")
    print(f"{'框架':10s} | {'生态':4s} | {'效率':4s} | {'可控':4s} | {'性能':4s}")
    for fw in matrix.frameworks:
        scores = [matrix.get_score(fw, d) for d in matrix.dimensions]
        print(f"{fw:10s} | {scores[0]:4d} | {scores[1]:4d} | {scores[2]:4d} | {scores[3]:4d}")

    print("\n=== 加权推荐演示 ===")
    weights_cases = [
        ({"生态成熟度": 0.4, "工程效率": 0.3, "可控性": 0.2, "性能": 0.1}, "原型验证（生态权重高）"),
        ({"生态成熟度": 0.1, "工程效率": 0.2, "可控性": 0.5, "性能": 0.2}, "核心商业（可控权重高）"),
        ({"生态成熟度": 0.3, "工程效率": 0.4, "可控性": 0.1, "性能": 0.2}, "短平快（效率权重高）"),
        ({"生态成熟度": 0.2, "工程效率": 0.2, "可控性": 0.3, "性能": 0.3}, "高性能场景（性能权重高）"),
    ]
    for weights, label in weights_cases:
        best, score, rankings = matrix.recommend(weights)
        print(f"\n--- {label} ---")
        print(f"  权重: 生态{weights['生态成熟度']:.0%} + 效率{weights['工程效率']:.0%} + 可控{weights['可控性']:.0%} + 性能{weights['性能']:.0%}")
        print(f"  → 推荐: {best}（总分 {score:.1f}）")
        print(f"  排名: {[(f'{f}:{s:.1f}') for f, s in rankings[:3]]}")


if __name__ == "__main__":
    main()
