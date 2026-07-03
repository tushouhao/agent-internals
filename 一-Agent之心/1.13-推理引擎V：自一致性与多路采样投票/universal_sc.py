# universal_sc
# 运行: python universal_sc.py

class UniversalSelfConsistency:
    """Universal SC: LLM 投票"""
    def __init__(self, llm, n_samples=10, temperature=0.7):
        self.llm = llm
        self.n_samples = n_samples
        self.temperature = temperature

    def solve(self, question):
        """采样后让 LLM 投票"""
        # 阶段 1: 多路采样
        chains = []
        for i in range(self.n_samples):
            chain = self.llm([{"role":"user","content":f"问题: {question}\n逐步推理。"}],
                            temp=self.temperature, seed=i)
            chains.append(chain)
        # 阶段 2: LLM 投票 (无需提取答案)
        return self._llm_vote(question, chains)

    def _llm_vote(self, question, chains):
        """LLM 阅读所有链后选最可信"""
        numbered = "\n".join(f"方案{i+1}: {c[:300]}..." for i, c in enumerate(chains))
        prompt = (f"问题: {question}\n以下是 {len(chains)} 个方案:\n{numbered}\n"
                  f"哪个方案的推理最严谨、答案最可信? 输出方案编号。")
        choice = self.llm([{"role":"user","content":prompt}])
        # 解析编号
        for i in range(len(chains), 0, -1):
            if f"方案{i}" in choice or str(i) in choice:
                return {"chain": chains[i-1], "choice": i, "method": "universal"}
        return {"chain": chains[0], "choice": 1, "method": "universal"}
if __name__ == "__main__":
    def llm(msgs, temp=0.7, seed=0):
        c = msgs[-1]["content"]
        if "逐步推理" in c:
            opts = ["方案: 用动态规划, 时间复杂度O(n)", "方案: 贪心算法, 简单但可能次优", "方案: 暴力枚举, O(2^n)"]
            return opts[seed % 3]
        if "哪个方案" in c: return "方案1: 动态规划最严谨"
        return "方案1"
    usc = UniversalSelfConsistency(llm, n_samples=3, temperature=0.7)
    r = usc.solve("找零钱最少硬币数")
    print(f"Universal SC 选择: 方案{r['choice']}")
    print(f"选中链: {r['chain'][:40]}...")

