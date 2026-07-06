# 文件名: build_vs_buy.py
# 功能: 自研 vs 用框架的三条判据决策器
# 运行: python build_vs_buy.py

"""自研 Harness 决策器：三条判据快速收敛。

判据1: 任务步数是否 > 20
判据2: 上下文策略是否需要非标准压缩
判据3: 工具数量是否 > 50 且需复杂权限
教学版，输入场景参数输出决策。
"""
from dataclasses import dataclass

@dataclass
class Decision:
    action: str       # 用框架 / 框架+扩展 / 自研
    reason: str
    risk: str         # 反例风险

def decide(task_steps: int, nonstandard_ctx: bool,
           tool_count: int, complex_rbac: bool) -> Decision:
    """三条判据决策。"""
    yes_count = 0
    reasons = []
    if task_steps > 20:
        yes_count += 1
        reasons.append(f"步数 {task_steps} > 20，需厚 harness 防长程崩溃")
    if nonstandard_ctx:
        yes_count += 1
        reasons.append("需非标准上下文压缩，框架 Memory 不够用")
    if tool_count > 50 and complex_rbac:
        yes_count += 1
        reasons.append(f"工具 {tool_count} 个且需细粒度 RBAC，框架权限太粗")

    if yes_count == 0:
        return Decision("用框架", "薄 harness 足够，框架省 5 倍工期",
                       "反例: 100步长程任务用LangChain，naive截断丢指令，失败率70%")
    elif yes_count == 1:
        return Decision("框架 + 扩展点", f"1条判据命中：{reasons[0]}",
                       "反例: 扩展点改超70%代码，不如自研")
    else:
        return Decision("自研", f"{yes_count}条判据命中：{'; '.join(reasons)}",
                       "反例: 5步任务自研，3周工期不如直接调框架")

SCENARIOS = [
    {"name": "客服 FAQ", "steps": 5, "ctx": False, "tools": 8, "rbac": False},
    {"name": "代码生成", "steps": 15, "ctx": False, "tools": 20, "rbac": False},
    {"name": "数据分析", "steps": 25, "ctx": True, "tools": 30, "rbac": False},
    {"name": "企业 RAG", "steps": 40, "ctx": True, "tools": 60, "rbac": True},
    {"name": "运维 Agent", "steps": 80, "ctx": True, "tools": 100, "rbac": True},
]

def main():
    print("=" * 72)
    print("自研 vs 用框架：三条判据决策器")
    print("=" * 72)
    print(f"{'场景':<14}{'步数':<6}{'工具':<6}{'决策':<16}{'理由'}")
    print("-" * 72)
    for s in SCENARIOS:
        d = decide(s["steps"], s["ctx"], s["tools"], s["rbac"])
        print(f"{s['name']:<14}{s['steps']:<6}{s['tools']:<6}{d.action:<16}{d.reason[:35]}")
    print()
    print("反例警示:")
    print("  过度工程: 5步任务自研 → 3周工期不如直接调LangChain")
    print("  框架选错: 100步任务用LangChain → naive截断丢指令,失败率70%")
    print("  两条都源于凭直觉决策，未用判据量化。")

if __name__ == "__main__":
    main()
