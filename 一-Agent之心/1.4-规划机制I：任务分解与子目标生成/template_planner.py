# template_planner
# 运行: python template_planner.py

PLAN_TEMPLATES = {
    "order_refund": {
        "description": "订单退款处理流程",
        "steps": [
            {"name": "verify_order", "action": "query_order", "depends": []},
            {"name": "check_refund_policy", "action": "get_refund_policy",
             "depends": ["verify_order"]},
            {"name": "process_refund", "action": "execute_refund",
             "depends": ["check_refund_policy"]},
            {"name": "notify_customer", "action": "send_notification",
             "depends": ["process_refund"]},
        ],
        "fallback": "escalate_to_human"
    },
    "data_report": {
        "description": "数据报告生成流程",
        "steps": [
            {"name": "collect_data", "action": "query_database", "depends": []},
            {"name": "analyze_trends", "action": "run_analysis",
             "depends": ["collect_data"]},
            {"name": "generate_chart", "action": "create_visualization",
             "depends": ["analyze_trends"]},
            {"name": "write_summary", "action": "llm_summarize",
             "depends": ["analyze_trends", "generate_chart"]},
        ]
    }
}

def match_template(goal, templates):
    """根据目标文本匹配模板（关键词规则）"""
    keywords = {
        "order_refund": ["退款", "订单", "退货"],
        "data_report": ["报告", "数据", "报表", "分析"],
    }
    for tmpl_id, kws in keywords.items():
        if any(kw in goal for kw in kws):
            return templates.get(tmpl_id)
    return None

def populate_template(template, goal):
    """填充模板，返回具体计划"""
    return {
        "matched": True,
        "description": template["description"],
        "goal": goal,
        "steps": template["steps"],
        "fallback": template.get("fallback"),
    }

def general_planner(goal):
    """通用回退规划"""
    return {
        "matched": False,
        "goal": goal,
        "steps": [{"name": "understand", "action": "llm_reason", "depends": []}],
    }

def template_planner(goal, templates):
    """基于模板的任务规划"""
    matched_template = match_template(goal, templates)
    if matched_template:
        return populate_template(matched_template, goal)
    return general_planner(goal)

if __name__ == "__main__":
    goals = [
        "处理订单 OD2024001 的退款",
        "生成本月销售数据报告",
        "查询天气预报",  # 无模板匹配
    ]
    print("=== 模板规划器 ===")
    for g in goals:
        plan = template_planner(g, PLAN_TEMPLATES)
        print(f"\n目标: {g}")
        print(f"  匹配: {plan['matched']}")
        print(f"  步骤数: {len(plan['steps'])}")
        for s in plan["steps"]:
            print(f"    - {s['name']} -> {s['action']}")
