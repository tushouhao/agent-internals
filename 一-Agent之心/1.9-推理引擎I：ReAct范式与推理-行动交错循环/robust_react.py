# robust_react
# 运行: python robust_react.py
import re, time

class TraceLogger:
    """内联依赖: 轨迹记录器"""
    def __init__(self):
        self.traces = []
    def log_step(self, step, thought, action, observation, metadata=None):
        self.traces.append({"step": step, "thought": thought,
                            "action": action, "observation": observation,
                            "metadata": metadata or {}})


class RobustReAct:
    """生产级 ReAct 引擎"""
    def __init__(self, llm, tools, config=None):
        cfg = config or {}
        self.llm = llm
        self.tools = tools
        self.max_steps = cfg.get("max_steps", 8)
        self.max_context_tokens = cfg.get("max_context", 8000)
        self.error_recovery = cfg.get("error_recovery", "retry")
        self.trace = TraceLogger()

    def run(self, query):
        history = [{"role": "user", "content": self._build_prompt(query)}]
        for step in range(self.max_steps):
            if self._estimate_tokens(history) > self.max_context_tokens:
                history = self._compress_history(history)
            try:
                response = self.llm(history)
            except Exception as e:
                if self.error_recovery == "retry":
                    continue
                return {"error": str(e), "step": step}
            history.append({"role": "assistant", "content": response})
            action = self._parse_action(response)
            self.trace.log_step(step, response, action, None)
            if action is None:
                return {"answer": response, "steps": step + 1}
            obs = self._safe_execute(action)
            history.append({"role": "tool", "content": obs})
            self.trace.traces[-1]["observation"] = obs

    def _build_prompt(self, query):
        tools_desc = "\n".join(f"- {n}: {(getattr(t,'__doc__','') or '')[:50]}"
                               for n, t in self.tools.items())
        return f"问题: {query}\n工具:\n{tools_desc}\n格式: Thought/Action/Observation"

    def _parse_action(self, response):
        m = re.search(r'Action:\s*(\w+)\[(.*?)\]', response)
        return {"tool": m.group(1), "args": m.group(2).strip()} if m else None

    def _estimate_tokens(self, history):
        return sum(len(m["content"]) // 2 for m in history)

    def _compress_history(self, history):
        if len(history) <= 4:
            return history
        head, tail = history[:2], history[-2:]
        mid_summary = f"[中间 {len(history)-4} 步已摘要]"
        return head + [{"role": "system", "content": mid_summary}] + tail

    def _safe_execute(self, action):
        try:
            tool = self.tools.get(action["tool"])
            return f"Observation: {tool(action['args'])}" if tool else f"Observation: 未知工具"
        except Exception as e:
            return f"Observation: 执行错误 {e}"

if __name__ == "__main__":
    def mock_llm(history):
        last = history[-1].get("content","")
        if "Observation" in last:
            return "Thought: 综合结果\nAnswer: 完成"
        return "Thought: 开始\nAction: search[test]"
    tools = {"search": lambda q: f"结果: {q}"}
    eng = RobustReAct(mock_llm, tools, {"max_steps":3, "max_context":1000})
    r = eng.run("测试任务")
    print(f"结果: {r.get('answer','')[:50]}")
    print(f"步数: {r.get('steps',0)}")

