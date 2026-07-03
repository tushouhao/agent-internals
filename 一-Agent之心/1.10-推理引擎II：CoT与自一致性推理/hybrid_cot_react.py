# hybrid_cot_react
# 运行: python hybrid_cot_react.py

class HybridCoTReAct:
    """CoT + ReAct 融合引擎"""
    def __init__(self, llm, tools, config=None):
        cfg = config or {}
        self.llm = llm
        self.tools = tools
        self.max_steps = cfg.get("max_steps", 6)
        self.cot_threshold = cfg.get("cot_threshold", 2)
        self.use_self_consistency = cfg.get("sc", False)
        self.sc_samples = cfg.get("sc_samples", 3)

    def run(self, query):
        """融合执行: ReAct 外环 + CoT 内核"""
        history = [{"role": "user", "content": query}]
        for step in range(self.max_steps):
            if self.use_self_consistency:
                thought = self._cot_with_sc(query, history)
            else:
                thought = self._single_cot(query, history)
            history.append({"role": "assistant", "content": thought})
            import re
            action_m = re.search(r'Action:\s*(\w+)\[(.*?)\]', thought)
            if not action_m:
                ans_m = re.search(r'Answer:\s*(.+)', thought, re.DOTALL)
                return {"answer": ans_m.group(1).strip() if ans_m else thought,
                        "steps": step + 1, "mode": "hybrid"}
            action = {"tool": action_m.group(1), "args": action_m.group(2).strip()}
            obs = self._execute(action)
            history.append({"role": "tool", "content": f"Observation: {obs}"})
        return {"answer": "未完成", "steps": self.max_steps, "mode": "hybrid"}

    def _single_cot(self, query, history):
        prompt = "请用 Chain-of-Thought 推理。格式: Thought/Action/Answer"
        full = history + [{"role": "system", "content": prompt}]
        return self.llm(full)

    def _cot_with_sc(self, query, history):
        """自一致性 CoT 内核"""
        chains = []
        for _ in range(self.sc_samples):
            resp = self._single_cot(query, history)
            chains.append(resp)
        from collections import Counter
        return max(chains, key=len)

    def _execute(self, action):
        tool = self.tools.get(action["tool"])
        return tool(action["args"]) if tool else f"未知工具 {action['tool']}"
if __name__ == "__main__":
    def llm(msgs):
        last = msgs[-1].get("content","")
        if "Observation" in last: return "Thought: 综合\nAnswer: 42"
        return "Thought: 需查询\nAction: search[q]"
    tools = {"search": lambda q: "42"}
    h = HybridCoTReAct(llm, tools, {"max_steps":3, "sc":True, "sc_samples":2})
    print(h.run("答案是什么?"))
