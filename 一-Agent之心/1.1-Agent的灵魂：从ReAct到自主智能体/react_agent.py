# react_agent
# 运行: python react_agent.py

class ReActAgent:
    """ReAct 范式 Agent"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def solve(self, question):
        """ReAct 交错循环"""
        trajectory = []
        prompt = self._build_prompt(question, trajectory)
        for step in range(10):
            # Thought-Action 交错生成
            response = self.llm([{"role": "user", "content": prompt}])
            thought, action = self._parse(response)
            trajectory.append({"thought": thought, "action": action})
            if action["name"] == "Finish":
                return {"answer": action.get("answer", ""), "steps": step + 1}
            # Observation
            obs = self._run_tool(action)
            trajectory.append({"observation": obs})
            prompt = self._build_prompt(question, trajectory)
        return {"answer": "未完成", "steps": 10}

    def _build_prompt(self, question, trajectory):
        """构建 ReAct 提示"""
        base = f"问题: {question}\n按 Thought/Action/Observation 格式推理。\n"
        for t in trajectory:
            if "thought" in t:
                base += f"\nThought: {t['thought']}\nAction: {t['action']['name']}[{t['action'].get('args','')}]"
            else:
                base += f"\nObservation: {t['observation']}"
        return base

    def _parse(self, response):
        """解析 Thought 和 Action"""
        thought = response.split("Action:")[0].replace("Thought:", "").strip()
        action_line = response.split("Action:")[-1].strip() if "Action:" in response else "Finish[]"
        name = action_line.split("[")[0].strip()
        args = action_line.split("[")[-1].rstrip("]") if "[" in action_line else ""
        if name == "Finish":
            return thought, {"name": "Finish", "answer": args}
        return thought, {"name": name, "args": args}

    def _run_tool(self, action):
        """执行工具"""
        tool = self.tools.get(action["name"])
        return tool(action["args"]) if tool else f"工具 {action['name']} 不存在"
if __name__ == "__main__":
    def llm(msgs):
        c = msgs[-1]["content"]
        if "格式推理" in c and len(c) < 100:
            return "Thought: 需先搜索\nAction: search[ReAct]"
        if "search" in c:
            return "Thought: 得到答案 42\nAction: Finish[42]"
        return "Thought: 直接回答\nAction: Finish[未知]"
    tools = {"search": lambda q: f"关于 {q} 的结果: 42"}
    agent = ReActAgent(llm, tools)
    r = agent.solve("什么是 ReAct?")
    print(f"答案: {r['answer']}, 步数: {r['steps']}")

