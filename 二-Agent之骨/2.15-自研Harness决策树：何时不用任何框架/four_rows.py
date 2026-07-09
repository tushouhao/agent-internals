# 文件名: four_rows.py
# 功能: 框架生态四横排对照表生成（教学版）
# 运行: python four_rows.py

"""四横排框架生态对照骨架。"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FrameworkRow:
    """横排项: 代表/工程量/红线出处/适用甜点。"""
    name: str
    rep: List[str]
    loc_range: str
    redline_src: str
    sweet_spot: str


@dataclass
class ProjectProfile:
    """项目画像: 四横排选型的输入。"""
    task_life_months: int
    script_or_prod: str
    debug_transparency_req: float
    vendor_lock_tolerance: float
    team_size: int


def recommend_row(profile: ProjectProfile) -> str:
    """据项目画像初判横排（教学版简化判据）。"""
    if profile.task_life_months < 3 and profile.script_or_prod == "script":
        return "托管（短平快省工程，2.13 短平快甜点）"
    if profile.debug_transparency_req >= 0.70 and profile.vendor_lock_tolerance <= 0.30:
        return "全自研（调式透明高 + 厂商依赖低，2.1-2.4 loop 工程）"
    if profile.team_size >= 2 and profile.task_life_months >= 6:
        return "框架内（团队协作 + �期项目，2.8-2.12）"
    return "协议层（互操作需求，2.14 MCP）"


def main():
    """四横排对照与初判演示。"""
    rows = [
        FrameworkRow("框架内", ["LangChain", "LangGraph", "LlamaIndex", "AutoGen", "CrewAI"],
                     "80-200 行", "2.8/2.9/2.10/2.11/2.12",
                     "团队协作的中期项目（2-5 人，3-12 月）"),
        FrameworkRow("托管", ["OpenAI Assistants", "Anthropic Tools", "Bedrock Agents"],
                     "10-80 行", "2.13",
                     "短平快任务/原型验证/单次脚本（<3 月）"),
        FrameworkRow("协议层", ["MCP tools", "MCP resources", "MCP prompts"],
                     "120-240 行", "2.14",
                     "跨 Agent 互操作/工具复用 ≥3 家客户端"),
        FrameworkRow("全自研", ["minimal harness"],
                     "280-450 行", "2.1-2.4",
                     "核心商业逻辑/合规要本地/定制 loop 深度（调式透明 ≥70%）"),
    ]

    print("=== 框架生态四横排 ===")
    print(f"{'横排':6s} | {'代表':50s} | {'工程量':12s} | {'红线出处':18s} | 甜点")
    for r in rows:
        rep_str = ",".join(r.rep)
        print(f"{r.name:6s} | {rep_str:50s} | {r.loc_range:12s} | {r.redline_src:18s} | {r.sweet_spot}")

    print("\n=== 散点判据困局 ===")
    print("卷二前 14 篇每篇给红线，散在七篇:")
    print("  2.8 链式三红线 / 2.9 图式四红线 / 2.10 检索三红线 / 2.11 对话三红线 / 2.12 角色三红线")
    print("  2.13 托管三红线（调敏/具敏/成敏） / 2.14 协议四红线（互操作/复用/覆盖/滞后）")
    print("困局: 新项目选型要翻七篇交叉对照，决策成本高")

    print("\n=== 项目画像初判演示 ===")
    cases = [
        ProjectProfile(1, "script", 0.50, 0.80, 1),
        ProjectProfile(12, "prod", 0.80, 0.20, 3),
        ProjectProfile(6, "prod", 0.60, 0.50, 2),
        ProjectProfile(8, "prod", 0.70, 0.40, 1),
    ]
    labels = ["场景A 短期脚本", "场景B 长期核心商业", "场景C 中期团队协作", "场景D 跨 Agent 互操作"]
    for label, prof in zip(labels, cases):
        rec = recommend_row(prof)
        print(f"  {label}: 寿命{prof.task_life_months}月 | {prof.script_or_prod} | 调式{prof.debug_transparency_req:.0%} | 厂商容忍{prof.vendor_lock_tolerance:.0%} | 团队{prof.team_size}人")
        print(f"    → 初判: {rec}")


if __name__ == "__main__":
    main()
