# trace_logger
# 运行: python trace_logger.py

class TraceLogger:
    """推理轨迹记录器"""
    def __init__(self):
        self.traces = []

    def log_step(self, step, thought, action, observation, metadata=None):
        """记录单步轨迹"""
        entry = {
            "step": step,
            "thought": thought,
            "action": action,
            "observation": observation,
            "timestamp": __import__("time").time(),
            "metadata": metadata or {},
        }
        self.traces.append(entry)

    def summarize(self):
        """生成轨迹摘要"""
        if not self.traces:
            return {"total_steps": 0}
        actions = [t["action"] for t in self.traces if t["action"]]
        return {
            "total_steps": len(self.traces),
            "action_count": len(actions),
            "unique_actions": len(set(str(a) for a in actions)),
            "avg_thought_len": sum(len(t["thought"]) for t in self.traces) / len(self.traces),
            "has_repeat": len(actions) != len(set(str(a) for a in actions)),
        }

    def find_anomaly(self):
        """检测轨迹异常"""
        anomalies = []
        action_strs = [str(t["action"]) for t in self.traces if t["action"]]
        for i, a in enumerate(action_strs):
            if action_strs.count(a) > 1:
                anomalies.append({"type": "repeat", "step": i, "action": a})
        for t in self.traces:
            if t["observation"] and "错误" in str(t["observation"]):
                anomalies.append({"type": "error_obs", "step": t["step"]})
        for t in self.traces:
            if len(t["thought"]) > 500:
                anomalies.append({"type": "long_thought", "step": t["step"],
                                  "len": len(t["thought"])})
        return anomalies

    def replay(self, upto_step=None):
        """回放轨迹到指定步"""
        end = upto_step or len(self.traces)
        for t in self.traces[:end]:
            print(f"[步{t['step']}] Thought: {t['thought'][:80]}...")
            if t["action"]:
                print(f"         Action: {t['action']}")
            if t["observation"]:
                print(f"         Obs: {t['observation'][:80]}...")

if __name__ == "__main__":
    tl = TraceLogger()
    tl.log_step(0, "需要查询天气", {"tool":"weather","args":"北京"}, "Observation: 晴 25度")
    tl.log_step(1, "查询温度", {"tool":"weather","args":"北京"}, "Observation: 晴 25度")
    tl.log_step(2, "获得答案", None, None)
    print(f"摘要: {tl.summarize()}")
    print(f"异常: {tl.find_anomaly()}")
    print("--- 回放 ---")
    tl.replay(2)

