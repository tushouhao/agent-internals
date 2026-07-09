# 文件名: final_decision.py
# 功能: 收卷判据 四维加权 + 场景适配 + 生死级剪枝优先骨架
# 运行: python final_decision.py

"""收卷判据: 四维加权 + 场景适配 + 生死级剪枝优先。"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class ScenarioWeight:
    """场景权重: 名称/四维权重/是否生死级。"""
    name: str
    weights: Dict[str, float]
    is_life_death: bool = False


@dataclass
class ProjectContext:
    """项目上下文: 收卷判据输入。"""
    scenario: str
    is_core_business: bool = False
    compliance_local: bool = False
    needs_custom_depth: bool = False


FRAMEWORK_SCORES: Dict[str, Dict[str, int]] = {
    "LangChain": {"生态成熟度": 9, "工程效率": 7, "可控性": 5, "性能": 6},
    "LangGraph": {"生态成熟度": 7, "工程效率": 6, "可控性": 7, "性能": 6},
    "LlamaIndex": {"生态成熟度": 8, "工程效率": 7, "可控性": 6, "性能": 7},
    "AutoGen": {"生态成熟度": 7, "工程效率": 6, "可控性": 7, "性能": 5},
    "CrewAI": {"生态成熟度": 6, "工程效率": 7, "可控性": 6, "性能": 5},
    "托管": {"生态成熟度": 8, "工程效率": 9, "可控性": 2, "性能": 5},
    "MCP混合": {"生态成熟度": 6, "工程效率": 5, "可控性": 6, "性能": 7},
    "全自研": {"生态成熟度": 2, "工程效率": 3, "可控性": 9, "性能": 8},
}

SCENARIO_WEIGHTS: Dict[str, ScenarioWeight] = {
    "原型验证": ScenarioWeight("原型验证", {"生态成熟度": 0.4, "工程效率": 0.3, "可控性": 0.2, "性能": 0.1}),
    "核心商业": ScenarioWeight("核心商业", {"生态成熟度": 0.1, "工程效率": 0.2, "可控性": 0.5, "性能": 0.2}, True),
    "短平快": ScenarioWeight("短平快", {"生态成熟度": 0.3, "工程效率": 0.4, "可控性": 0.1, "性能": 0.2}),
    "高性能": ScenarioWeight("高性能", {"生态成熟度": 0.2, "工程效率": 0.2, "可控性": 0.3, "性能": 0.3}),
    "跨Agent协作": ScenarioWeight("跨Agent协作", {"生态成熟度": 0.3, "工程效率": 0.2, "可控性": 0.2, "性能": 0.3}),
    "合规本地": ScenarioWeight("合规本地", {"生态成熟度": 0.1, "工程效率": 0.2, "可控性": 0.6, "性能": 0.1}, True),
}


def compute_total(framework: str, weights: Dict[str, float]) -> float:
    """据四维权重算框架总评分。"""
    scores = FRAMEWORK_SCORES[framework]
    return sum(scores[dim] * weight for dim, weight in weights.items())


def rank_all(weights: Dict[str, float]) -> List[Tuple[str, float]]:
    """全框架排名。返回 [(框架, 总分)] 降序。"""
    rankings = [(fw, compute_total(fw, weights)) for fw in FRAMEWORK_SCORES]
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings


def final_decision(ctx: ProjectContext) -> Tuple[str, str, List[Tuple[str, float]]]:
    """收卷判据: 生死级剪枝优先 + 四维加权排名。返回 (推荐, 原因, 排名)。"""
    if ctx.is_core_business or ctx.compliance_local or ctx.needs_custom_depth:
        return "全自研", "生死级剪枝: 核心商业/合规本地/定制深度 → 全自研（承接 2.15）", []

    scenario = SCENARIO_WEIGHTS.get(ctx.scenario)
    if not scenario:
        return "全自研", "默认（未知场景）→ 全自研", []

    rankings = rank_all(scenario.weights)
    return rankings[0][0], f"场景「{ctx.scenario}」四维加权最高分", rankings


def main():
    """收卷判据演示。"""
    print("=== 六类场景权重对照 ===")
    print(f"{'场景':12s} | {'生态':6s} | {'效率':6s} | {'可控':6s} | {'性能':6s} | 生死级")
    for name, sw in SCENARIO_WEIGHTS.items():
        w = sw.weights
        print(f"{name:12s} | {w['生态成熟度']:.0%}    | {w['工程效率']:.0%}    | {w['可控性']:.0%}    | {w['性能']:.0%}    | {sw.is_life_death}")

    print("\n=== 收卷判据演示（生死级剪枝优先）===")
    cases = [
        ProjectContext("原型验证"),
        ProjectContext("核心商业", is_core_business=True),
        ProjectContext("短平快"),
        ProjectContext("高性能"),
        ProjectContext("跨Agent协作"),
        ProjectContext("合规本地", compliance_local=True),
    ]
    for ctx in cases:
        best, reason, rankings = final_decision(ctx)
        print(f"\n--- 场景: {ctx.scenario} ---")
        print(f"  核心商业={ctx.is_core_business} | 合规本地={ctx.compliance_local} | 定制深度={ctx.needs_custom_depth}")
        print(f"  → 推荐: {best}")
        print(f"  原因: {reason}")
        if rankings:
            top3 = [(f, round(s, 1)) for f, s in rankings[:3]]
            print(f"  Top3: {top3}")

    print("\n=== 卷二完结前瞻卷三 ===")
    print("卷二 17 篇拆「选哪类框架 + 框架内怎么编排 + 层级委托」:")
    print("  2.1-2.5 loop 工程四部曲立自研 harness 骨架")
    print("  2.6-2.7 Skill 工程化拆工具注册与调度")
    print("  2.8-2.12 拆五类编排范式（链/图/检索/对话/角色）")
    print("  2.13 托管式四崩点 + 2.14 协议层四红线")
    print("  2.15 决策树收散判据 + 2.16 层级委托纵向扩展")
    print("  2.17 四维评分矩阵收卷")
    print("卷三 Agent 之刃 14 篇转「框架内怎么实战」:")
    print("  从「选哪类框架」到「框架内实战场景」")
    print("  如 RAG 实战/对话实战/工具实战/多 Agent 实战等")

    print("\n=== 核心洞察 ===")
    print("四维评分矩阵不是劝全自研满分，是劝按场景权重选最高")
    print("生死级场景剪枝优先（承接 2.15）: 核心商业/合规本地/定制深度 → 全自研")
    print("效率级场景按权重: 原型验证生态权重高/短平快效率权重高/高性能性能权重高")
    print("横纵二分: 横向选型用矩阵（本篇）/ 纵向委托用层级（2.16）")


if __name__ == "__main__":
    main()
