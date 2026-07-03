# cot_variants
# 运行: python cot_variants.py

class CoTVariants:
    """CoT 三种变体实现"""
    def __init__(self, llm):
        self.llm = llm

    def zero_shot(self, query):
        """零样本 CoT: 仅加触发词"""
        prompt = f"{query}\n\n让我们一步步想。"
        return self.llm([{"role": "user", "content": prompt}])

    def few_shot(self, query, examples):
        """少样本 CoT: 提供推理示例"""
        prompt = ""
        for ex in examples:
            prompt += f"问题: {ex['question']}\n推理: {ex['reasoning']}\n答案: {ex['answer']}\n\n"
        prompt += f"问题: {query}\n推理:"
        return self.llm([{"role": "user", "content": prompt}])

    def self_consistency(self, query, n_samples=5, examples=None):
        """自一致性 CoT: 多链投票"""
        chains = []
        for i in range(n_samples):
            if examples:
                response = self.few_shot(query, examples)
            else:
                response = self.zero_shot(query)
            answer = self._extract_answer(response)
            chains.append({"reasoning": response, "answer": answer})
        return self._vote(chains)

    def _extract_answer(self, response):
        """从推理链中提取最终答案"""
        import re
        for pattern in [r'答案[:：]\s*(.+)', r'Answer[:：]\s*(.+)',
                        r'因此[，,]?\s*(.+)']:
            m = re.search(pattern, response)
            if m:
                return m.group(1).strip()
        return response[-50:].strip()

    def _vote(self, chains):
        """多数投票选择最终答案"""
        from collections import Counter
        answers = [c["answer"] for c in chains if c["answer"]]
        if not answers:
            return {"answer": None, "confidence": 0, "chains": chains}
        counter = Counter(answers)
        best, count = counter.most_common(1)[0]
        return {"answer": best, "confidence": count / len(answers),
                "chains": chains, "vote_distribution": dict(counter)}
if __name__ == "__main__":
    def llm(msgs): return "推理: 2+2=4\n答案: 4" if "一步步" in msgs[-1]["content"] else "4"
    cot = CoTVariants(llm)
    print(f"零样本: {cot.zero_shot('2+2=?')[:30]}")
    print(f"少样本: {cot.few_shot('2+2=?', [{'question':'1+1','reasoning':'1+1=2','answer':'2'}])[:30]}")
    print(f"自一致性: {cot.self_consistency('2+2=?', n_samples=3)}")
