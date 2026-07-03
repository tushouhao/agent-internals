# hierarchical_decomp
# 运行: python hierarchical_decomp.py

def hierarchical_decomposition(goal, tools, max_depth=3):
    """逐层分解：从高层目标到底层指令"""
    plan_tree = {"goal": goal, "children": [], "depth": 0}

    def decompose(node, depth):
        if depth >= max_depth:
            # 叶子节点：映射到工具调用
            node["action"] = map_to_tool(node["goal"], tools)
            return
        subgoals = llm_decompose(node["goal"])  # LLM 分解
        for sg in subgoals:
            child = {"goal": sg, "children": [], "depth": depth + 1}
            decompose(child, depth + 1)
            node["children"].append(child)

    decompose(plan_tree, 0)
    return plan_tree
