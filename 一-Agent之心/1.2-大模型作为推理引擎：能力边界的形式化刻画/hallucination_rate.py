# 幻觉率测量函数
# 运行: python hallucination_rate.py

def hallucination_rate(llm, queries, ground_truths, verifier_fn):
    """测量 LLM 在知识密集型任务上的幻觉率"""
    total, hallucinated = 0, 0
    for query, truth in zip(queries, ground_truths):
        response = llm(query)
        if verifier_fn(response, truth) < 0.5:
            hallucinated += 1
        total += 1
    return hallucinated / total
