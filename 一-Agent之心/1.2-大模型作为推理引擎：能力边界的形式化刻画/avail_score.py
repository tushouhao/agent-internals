# Avail 可用性评分
# 运行: python avail_score.py

def avail_score(task_features, llm_benchmarks):
    """计算推理任务的可用性评分(0-100)"""
    score = 100
    # 复杂度惩罚
    if task_features["complexity"] > 6:
        score -= 25
    # 知识开放性惩罚
    if task_features["knowledge_type"] == "open":
        score -= 15
    # 符号推理惩罚
    if task_features["requires_symbolic"]:
        score -= 30
    # 环境惩罚 (需要外部工具)
    if task_features["requires_tool"]:
        score += 10  # 有工具可降低
    # 安全惩罚
    if task_features["safety_critical"]:
        score -= 20
    return max(0, min(100, score))
