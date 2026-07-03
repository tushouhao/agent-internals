# agent_state
# 运行: python agent_state.py

class AgentState:
    """Agent 状态管理器"""
    def __init__(self, max_context=4000):
        self.max_context = max_context
        self.trajectory = []      # 完整轨迹 (Thought/Action/Observation)
        self.work_memory = {}     # 工作记忆 (中间结果)
        self.step_count = 0

    def add(self, entry):
        """添加轨迹条目"""
        self.trajectory.append(entry)
        self.step_count += 1
        # 上下文溢出时压缩
        if self._context_length() > self.max_context:
            self._compress()

    def set(self, key, value):
        """设置工作记忆"""
        self.work_memory[key] = value

    def get(self, key, default=None):
        """获取工作记忆"""
        return self.work_memory.get(key, default)

    def context_for_llm(self):
        """构建 LLM 上下文"""
        return "\n".join(self._format(e) for e in self.trajectory)

    def _context_length(self):
        return sum(len(self._format(e)) for e in self.trajectory)

    def _format(self, entry):
        if "thought" in entry: return f"Thought: {entry['thought']}"
        if "action" in entry: return f"Action: {entry['action']}"
        if "observation" in entry: return f"Observation: {entry['observation']}"
        return str(entry)

    def _compress(self):
        """压缩: 保留首尾, 摘要中间"""
        if len(self.trajectory) < 6: return
        head = self.trajectory[:2]
        tail = self.trajectory[-2:]
        middle = self.trajectory[2:-2]
        summary = f"[中间 {len(middle)} 步已摘要: " + \
                  "; ".join(self._format(m)[:30] for m in middle) + "]"
        self.trajectory = head + [{"summary": summary}] + tail
if __name__ == "__main__":
    state = AgentState(max_context=200)
    for i in range(8):
        state.add({"thought": f"第{i+1}步思考内容较长"*3})
        state.add({"action": f"action_{i}"})
        state.add({"observation": f"观察结果 {i} " * 10})
    state.set("中间结果", 42)
    print(f"步数: {state.step_count}, 工作记忆: {state.get('中间结果')}")
    print(f"压缩后轨迹: {len(state.trajectory)}条")
    ctx = state.context_for_llm()
    print(f"上下文长度: {len(ctx)} 字符")

