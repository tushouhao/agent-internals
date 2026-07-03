# agent_core
# 运行: python agent_core.py

import time

class Agent:
    """Agent 核心循环: 感知-规划-行动-观察"""
    def __init__(self, llm, tools, max_steps=10):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def run(self, user_input):
        """Agent 主循环"""
        self.history = [{"role": "user", "content": user_input}]
        for step in range(self.max_steps):
            # 阶段 1: 感知+推理 (Thought)
            thought = self._reason()
            self.history.append({"role": "assistant", "content": thought})
            # 阶段 2: 判断是否需要行动
            if self._is_final(thought):
                return self._extract_answer(thought)
            # 阶段 3: 行动 (Action)
            action = self._parse_action(thought)
            # 阶段 4: 观察 (Observation)
            observation = self._execute(action)
            self.history.append({"role": "tool", "content": observation})
        return "达到最大步数, 未能完成任务"

    def _reason(self):
        """LLM 推理: 基于历史决定下一步"""
        return self.llm(self.history)

    def _is_final(self, thought):
        """判断是否为最终答案"""
        return "答案:" in thought or "最终" in thought

    def _parse_action(self, thought):
        """解析动作"""
        if "搜索" in thought: return {"tool": "search", "query": thought}
        if "计算" in thought: return {"tool": "calc", "expr": thought}
        return {"tool": "none", "query": thought}

    def _execute(self, action):
        """执行工具调用"""
        tool = self.tools.get(action["tool"])
        return tool(action) if tool else "无可用工具"

    def _extract_answer(self, thought):
        """提取最终答案"""
        for marker in ["答案:", "最终答案:"]:
            if marker in thought:
                return thought.split(marker)[-1].strip()
        return thought
if __name__ == "__main__":
    def llm(history):
        last = history[-1].get("content","")
        if "搜索" in last or "查询" in last:
            return "Thought: 需要搜索\nAction: search[相关信息]\n"
        return "答案: 42"
    tools = {
        "search": lambda a: "搜索结果: 42 是答案",
        "calc": lambda a: "计算结果: 42",
    }
    agent = Agent(llm, tools, max_steps=5)
    result = agent.run("查询并计算答案")
    print(f"结果: {result}")
    print(f"历史步数: {len(agent.history)}")

