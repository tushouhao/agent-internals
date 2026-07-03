# self_consistency
# 运行: python self_consistency.py

from collections import Counter

class SelfConsistency:
    """自一致性多路采样投票"""
    def __init__(self, llm, n_samples=10, temperature=0.7):
        self.llm = llm
        self.n_samples = n_samples
        self.temperature = temperature

    def solve(self, question):
        """采样-投票双引擎"""
        # 阶段 1: 多路采样
        samples = []
        for i in range(self.n_samples):
            chain = self._sample_chain(question, seed=i)
            answer = self._extract_answer(chain)
            samples.append({"chain": chain, "answer": answer})
        # 阶段 2: 投票
        answers = [s["answer"] for s in samples if s["answer"] is not None]
        if not answers:
            return None, samples
        tally = Counter(answers)
        final, votes = tally.most_common(1)[0]
        return {"answer": final, "votes": votes, "total": len(answers),
                "confidence": votes / len(answers)}, samples

    def _sample_chain(self, question, seed):
        """采样单条推理链 (高温)"""
        prompt = f"问题: {question}\n请逐步推理并给出答案。"
        # 模拟高温采样的多样性
        return self.llm([{"role": "user", "content": prompt}], temp=self.temperature, seed=seed)

    def _extract_answer(self, chain):
        """从推理链提取最终答案"""
        for marker in ["答案是", "答案:", "最终答案"]:
            if marker in chain:
                idx = chain.index(marker) + len(marker)
                return chain[idx:idx+20].strip().split()[0] if idx < len(chain) else None
        return None
if __name__ == "__main__":
    def llm(msgs, temp=0.7, seed=0):
        opts = ["答案是42 步骤: 6*7", "答案是42 验算: 42/6=7", "答案是36 错误推理", "答案是42", "答案是42 复查OK"]
        return opts[seed % len(opts)]
    sc = SelfConsistency(llm, n_samples=5, temperature=0.7)
    result, samples = sc.solve("6乘7等于多少?")
    print(f"最终答案: {result['answer']}, 票数: {result['votes']}/{result['total']}, 置信度: {result['confidence']:.0%}")

