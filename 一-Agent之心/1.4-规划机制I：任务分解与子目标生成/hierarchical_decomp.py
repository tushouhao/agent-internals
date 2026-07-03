# hierarchical_decomp
# 运行: python hierarchical_decomp.py

# 简化版 LLM 分解：基于关键词的规则分解
def llm_decompose(goal):
    """将目标分解为子目标（规则模拟 LLM）"""
    if "并" in goal:
        parts = goal.split("并")
        return [p.strip() for p in parts if p.strip()]
    if "调研" in goal or "研究" in goal:
        return ["收集资料", "分析整理", "形成结论"]
    if "发邮件" in goal or "汇报" in goal:
        return ["撰写内容", "确定收件人", "发送邮件"]
    return [f"执行 {goal}"]

def map_to_tool(subgoal, tools):
    """将子目标映射到工具"""
    if "收集" in subgoal or "资料" in subgoal:
        return tools[0] if "search" in tools else tools[0]
    if "分析" in subgoal:
        return "summarize" if "summarize" in tools else tools[-1]
    if "发" in subgoal or "邮件" in subgoal:
        return "send_email" if "send_email" in tools else tools[-1]
    return tools[0]

def hierarchical_decomposition(goal, tools, max_depth=3):
    """逐层分解：从高层目标到底层指令"""
    plan_tree = {"goal": goal, "children": [], "depth": 0}

    def decompose(node, depth):
        if depth >= max_depth:
            node["action"] = map_to_tool(node["goal"], tools)
            return
        subgoals = llm_decompose(node["goal"])
        if not subgoals or subgoals == [node["goal"]]:
            node["action"] = map_to_tool(node["goal"], tools)
            return
        for sg in subgoals:
            child = {"goal": sg, "children": [], "depth": depth + 1}
            decompose(child, depth + 1)
            node["children"].append(child)

    decompose(plan_tree, 0)
    return plan_tree

def print_tree(node, indent=0):
    """递归打印树结构"""
    prefix = "  " * indent
    if "action" in node:
        print(f"{prefix}- [叶] {node['goal']} -> 工具: {node['action']}")
    else:
        print(f"{prefix}+ [目标] {node['goal']} (深度{node['depth']})")
        for c in node["children"]:
            print_tree(c, indent + 1)

if __name__ == "__main__":
    tools = ["search", "summarize", "send_email"]
    print("=== 层次分解: 调研 RAG 并发邮件汇报 ===")
    tree = hierarchical_decomposition("调研 RAG 并发邮件汇报", tools, max_depth=3)
    print_tree(tree)
