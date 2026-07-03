# cot_vs_react
# 运行: python cot_vs_react.py

class CoTEngine:
    """纯 Chain-of-Thought 推理引擎"""
    def __init__(self, llm):
        self.llm = llm

    def run(self, query):
        prompt = f"""问题: {query}
请一步步推理，最后给出答案。
格式:
Thought: <推理步骤>
...
Answer: <最终答案>"""
        response = self.llm([{"role": "user", "content": prompt}])
        return {"answer": response, "type": "cot"}


class ReActEngine:
    """ReAct 推理引擎（对比实现）"""
    def __init__(self, llm, tools, max_steps=6):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps

    def run(self, query):
        prompt = f"""问题: {query}
可用工具: {list(self.tools.keys())}
格式:
Thought: <推理>
Action: tool_name[args]
Observation: <工具返回>
... (重复)
Thought: <最终推理>
Answer: <最终答案>"""
        history = [{"role": "user", "content": prompt}]
        for step in range(self.max_steps):
            response = self.llm(history)
            history.append({"role": "assistant", "content": response})
            if "Answer:" in response:
                import re
                m = re.search(r'Answer:\s*(.+)', response, re.DOTALL)
                return {"answer": m.group(1).strip() if m else response,
                        "steps": step + 1, "type": "react"}
            action = self._parse_action(response)
            if not action:
                return {"answer": response, "steps": step + 1, "type": "react"}
            obs = self._execute(action)
            history.append({"role": "user",
                            "content": f"Observation: {obs}"})
        return {"answer": "未终止", "steps": self.max_steps, "type": "react"}

    def _parse_action(self, response):
        import re
        m = re.search(r'Action:\s*(\w+)\[(.*?)\]', response)
        return {"tool": m.group(1), "args": m.group(2).strip()} if m else None

    def _execute(self, action):
        tool = self.tools.get(action["tool"])
        return tool(action["args"]) if tool else f"未知工具 {action['tool']}"

if __name__ == "__main__":
    def llm_cot(msgs):
        return "Thought: 2+2=4\nAnswer: 4"
    def llm_react(msgs):
        last = msgs[-1].get("content","")
        if "Observation" in last:
            return "Thought: 综合以上\nAnswer: 42"
        return "Thought: 需查证\nAction: calc[2+2]"
    cot = CoTEngine(llm_cot)
    print(f"CoT: {cot.run('2+2=?')}")
    react = ReActEngine(llm_react, {"calc": lambda e: "4"}, max_steps=3)
    print(f"ReAct: {react.run('2+2=?')}")

