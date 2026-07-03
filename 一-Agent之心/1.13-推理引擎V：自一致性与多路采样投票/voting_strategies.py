# voting_strategies
# 运行: python voting_strategies.py

from collections import defaultdict, Counter

class VotingStrategies:
    """四种投票策略"""
    def majority_vote(self, samples):
        """多数投票: 票数最高"""
        answers = [s["answer"] for s in samples if s["answer"]]
        return Counter(answers).most_common(1)[0][0] if answers else None

    def weighted_vote(self, samples):
        """加权投票: 按推理链长度加权 (长链更可信)"""
        weights = defaultdict(float)
        for s in samples:
            if s["answer"]:
                w = 1.0 + min(len(s["chain"]) / 1000, 1.0)
                weights[s["answer"]] += w
        return max(weights, key=weights.get) if weights else None

    def confidence_vote(self, samples, llm):
        """置信度投票: LLM 评估每条链的可信度"""
        scores = defaultdict(float)
        for s in samples:
            if s["answer"]:
                conf = self._confidence(s["chain"], llm)
                scores[s["answer"]] += conf
        return max(scores, key=scores.get) if scores else None

    def layer_vote(self, samples):
        """分层投票: 按答案类型分组再组内投票"""
        groups = defaultdict(list)
        for s in samples:
            if s["answer"]:
                atype = self._answer_type(s["answer"])
                groups[atype].append(s)
        # 每组选代表答案
        group_answers = []
        for atype, group in groups.items():
            tally = Counter(s["answer"] for s in group)
            group_answers.append(tally.most_common(1)[0])
        # 组间按组大小加权
        return max(group_answers, key=lambda x: x[1])[0] if group_answers else None

    def _confidence(self, chain, llm):
        prompt = f"推理链: {chain[:200]}\n这条推理的可信度 0-1:"
        resp = llm([{"role": "user", "content": prompt}])
        try: return float(resp.strip())
        except: return 0.5

    def _answer_type(self, answer):
        if answer.replace('.', '').replace('-', '').isdigit(): return "numeric"
        if len(answer) < 10: return "short"
        return "long"

    def 分层_vote(self, samples):
        return self.layer_vote(samples)
if __name__ == "__main__":
    def llm(msgs): return "0.8"
    vs = VotingStrategies()
    samples = [
        {"answer": "A", "chain": "长推理链"*20},
        {"answer": "A", "chain": "短链"},
        {"answer": "B", "chain": "中等长度链"*10},
        {"answer": "A", "chain": "另一个长链"*15},
        {"answer": "B", "chain": "短链2"},
    ]
    print(f"多数投票: {vs.majority_vote(samples)}")
    print(f"加权投票: {vs.weighted_vote(samples)}")
    print(f"置信度投票: {vs.confidence_vote(samples, llm)}")
    print(f"分层投票: {vs.layer_vote(samples)}")

