# react_loop
# 运行: python react_loop.py

class ReActLoop:
    """ReAct 推理-行动交错循环"""
    def __init__(self, llm, tools, max_steps=8):
        self.llm = llm
        self.tools = tools  # {name: callable}
        self.max_steps = max_steps
        self.history = []   # 完整轨迹

    def run(self, query):
        """执行 ReAct 循环"""
        self.history = [{"role": "user", "content": query}]
        for step in range(self.max_steps):
            response = self.llm(self.history)
            self.history.append({"role": "assistant", "content": response})

            action = self._parse_action(response)

            if action is None:
                return {"answer": response, "steps": step + 1,
                        "trace": self.history}

            observation = self._execute(action)
            self.history.append({"role": "tool", "content": observation,
                                 "tool_call": action})

        return {"answer": "达到最大步数", "steps": self.max_steps,
                "trace": self.history, "truncated": True}

    def _parse_action(self, response):
        """从 LLM 响应中解析行动"""
        import re
        m = re.search(r'Action:\s*(\w+)\[(.*?)\]', response)
        if not m:
            return None  # 无行动 = 终止
        return {"tool": m.group(1), "args": m.group(2).strip()}

    def _execute(self, action):
        """执行工具调用"""
        tool = self.tools.get(action["tool"])
        if not tool:
            return f"错误: 未知工具 {action['tool']}"
        try:
            result = tool(action["args"])
            return f"Observation: {result}"
        except Exception as e:
            return f"Observation: 执行失败 {e}"

if __name__ == "__main__":
    def mock_llm(history):
        last = history[-1].get("content","")
        if "完成" in last or "Observation: 42" in last:
            return "Thought: 已获得答案\nAnswer: 42"
        if "Action" not in last:
            return "Thought: 需要查询\nAction: search[答案]"
        return "Thought: 分析中"
    tools = {"search": lambda q: f"结果: {q} -> 42"}
    loop = ReActLoop(mock_llm, tools, max_steps=5)
    r = loop.run("宇宙的答案是什么?")
    print(f"答案: {r['answer'][:60]}")
    print(f"步数: {r['steps']}")

