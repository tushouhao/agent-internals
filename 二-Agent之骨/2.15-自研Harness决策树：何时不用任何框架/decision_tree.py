# 文件名: decision_tree.py
# 功能: 决策树根→枝→叶三层骨架 + 可遍历结构
# 运行: python decision_tree.py

"""选型决策树骨架: 根问要不要用框架，三枝分流，叶节点给具体选型。"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class LeafNode:
    """叶节点: 具体选型 + 工程量 + 承接出处。"""
    name: str
    loc: str
    carry_from: str
    sweet_spot: str


@dataclass
class BranchNode:
    """枝节点: 分岔问题 + 判据 + 叶子清单。"""
    name: str
    question: str
    criteria: str
    leaves: Dict[str, LeafNode] = field(default_factory=dict)

    def add_leaf(self, key: str, leaf: LeafNode) -> None:
        self.leaves[key] = leaf


@dataclass
class DecisionTree:
    """决策树: 根 + 三枝 + 可遍历接口。"""
    root_question: str
    root_criteria: str
    branches: Dict[str, BranchNode] = field(default_factory=dict)

    def add_branch(self, key: str, branch: BranchNode) -> None:
        self.branches[key] = branch

    def traverse(self, project: Dict[str, Any]) -> List[str]:
        """遍历决策树给项目选型（教学版简化判据）。"""
        recommendations = []

        life = project.get("task_life_months", 0)
        loc = project.get("estimated_loc", 0)
        use_framework = life >= 3 and loc >= 280

        if not use_framework:
            recommendations.append("根判据不过 → 全自研 harness（280-450 行）")
            return recommendations

        recommendations.append(f"根判据通过（寿命{life}月 ≥3 + 工程{loc}行 ≥280）→ 借框架")

        if project.get("vendor_lock_tolerance", 0.5) >= 0.60:
            recommendations.append("枝一托管: 厂商容忍 ≥60% → 托管 loop（OpenAI Assistants 等）")
        else:
            recommendations.append("枝一自研: 厂商容忍 <60% → minimal harness loop 自研")

        if project.get("interop_ratio", 0.0) >= 0.30:
            recommendations.append("枝二上 MCP: 互操作占比 ≥30% → MCP server + 原生混合谱二")
        else:
            recommendations.append("枝二原生: 互操作占比 <30% → 框架内工具或自研工具")

        orchestration = project.get("orchestration_type", "图式")
        rec_map = {"链式": "LangChain（承接 2.8）", "图式": "LangGraph（承接 2.9）",
                   "检索": "LlamaIndex（承接 2.10）", "对话": "AutoGen（承接 2.11）",
                   "角色": "CrewAI（承接 2.12）"}
        recommendations.append(f"枝三编排: {orchestration} → {rec_map.get(orchestration, 'LangGraph 默认')}")

        return recommendations


def main():
    """决策树骨架与遍历演示。"""
    tree = DecisionTree(
        root_question="要不要用框架?",
        root_criteria="任务寿命 ≥3 月 AND 工程量 ≥280 行")

    b1 = BranchNode("loop托管", "loop 调度要不要托管?", "厂商依赖容忍 ≥60%")
    b1.add_leaf("托管", LeafNode("OpenAI Assistants", "10-80 行", "2.13", "短平快任务"))
    b1.add_leaf("自研", LeafNode("minimal harness loop", "280-450 行", "2.1-2.4", "核心商业逻辑"))
    tree.add_branch("枝一", b1)

    b2 = BranchNode("协议层", "工具要不要上 MCP?", "互操作任务占比 ≥30% AND 协议覆盖率 ≥85%")
    b2.add_leaf("上 MCP", LeafNode("MCP server + 原生混合谱二", "180 行", "2.14", "跨 Agent 协作"))
    b2.add_leaf("原生", LeafNode("框架内工具或自研工具", "50-200 行", "2.6/2.14", "内部任务为主"))
    tree.add_branch("枝二", b2)

    b3 = BranchNode("框架内编排", "选哪类编排范式?", "按任务结构：链/图/检索/对话/角色")
    b3.add_leaf("链式", LeafNode("LangChain", "80-160 行", "2.8", "线性流水任务"))
    b3.add_leaf("图式", LeafNode("LangGraph", "120-200 行", "2.9", "状态多分支任务"))
    b3.add_leaf("检索", LeafNode("LlamaIndex", "100-180 行", "2.10", "知识密集任务"))
    b3.add_leaf("对话", LeafNode("AutoGen", "100-200 行", "2.11", "多角色涌现任务"))
    b3.add_leaf("角色", LeafNode("CrewAI", "80-180 行", "2.12", "多角色显式契约任务"))
    tree.add_branch("枝三", b3)

    print("=== 决策树骨架 ===")
    print(f"根: {tree.root_question}")
    print(f"判据: {tree.root_criteria}")
    for bk, b in tree.branches.items():
        print(f"\n{bk}: {b.name}")
        print(f"  问题: {b.question}")
        print(f"  判据: {b.criteria}")
        for lk, leaf in b.leaves.items():
            print(f"  叶[{lk}]: {leaf.name} | {leaf.loc} | 承接 {leaf.carry_from} | 甜点 {leaf.sweet_spot}")

    print("\n=== 决策树遍历演示 ===")
    cases = [
        {"label": "场景A 长期核心商业", "task_life_months": 12, "estimated_loc": 500,
         "vendor_lock_tolerance": 0.20, "interop_ratio": 0.10, "orchestration_type": "图式"},
        {"label": "场景B 跨 Agent 协作平台", "task_life_months": 8, "estimated_loc": 350,
         "vendor_lock_tolerance": 0.40, "interop_ratio": 0.50, "orchestration_type": "图式"},
        {"label": "场景C 短期脚本", "task_life_months": 1, "estimated_loc": 80,
         "vendor_lock_tolerance": 0.80, "interop_ratio": 0.05, "orchestration_type": "链式"},
    ]
    for proj in cases:
        print(f"\n--- {proj['label']} ---")
        for line in tree.traverse(proj):
            print(f"  {line}")


if __name__ == "__main__":
    main()
