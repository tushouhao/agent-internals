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

if __name__ == "__main__":
    def mock_llm(q):
        return f"答案是 {q.split()[-1]} 相关"
    def mock_verify(a, gt):
        return gt.lower() in a.lower()

    queries = ["什么是 RAG", "Agent 是什么", "ToT 是什么"]
    truths = ["检索增强生成", "智能体", "思维树"]
    rate = hallucination_rate(mock_llm, queries, truths, mock_verify)
    print(f"幻觉率: {rate*100:.1f}%")
    print(f"评估: {'高' if rate > 0.3 else '中' if rate > 0.1 else '低'}")
