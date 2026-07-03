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

def template_planner(goal, templates):
    """基于模板的任务规划"""
    matched_template = match_template(goal, templates)
    if matched_template:
        return populate_template(matched_template, goal)
    # 无匹配模板时回退到通用规划
    return general_planner(goal)
