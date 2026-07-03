# security_audit_logger
# 运行: python security_audit_logger.py

import json, time
class SecurityAuditLogger:
    """安全审计日志器"""
    def __init__(self, log_path="audit.log"):
        self.log_path = log_path
        self.entries = []
    def log_action(self, agent_action, user_input, decision, context):
        """记录每个动作决策"""
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "action": agent_action,
            "input_hash": self._hash(user_input),
            "decision": decision,
            "context": context,
            "risk_level": context.get("risk_level", "unknown"),
        }
        self.entries.append(entry)
        self._persist(entry)
        return entry
    def trace_incident(self, incident_time, window_minutes=30):
        """事故追溯: 回放时间窗口内所有动作"""
        window = [e for e in self.entries
                  if self._within_window(e["timestamp"], incident_time, window_minutes)]
        return {
            "n_actions": len(window),
            "critical_actions": [e for e in window if e["risk_level"] == "critical"],
            "blocked_actions": [e for e in window if e["decision"].get("executed") is False],
            "timeline": window,
        }
    def detect_anomaly(self):
        """异常模式检测"""
        anomalies = []
        # 检测 1: 短时间大量危险动作
        danger_count = sum(1 for e in self.entries[-50:]
                          if e["risk_level"] in ["dangerous", "critical"])
        if danger_count > 10:
            anomalies.append({"type": "danger_burst", "count": danger_count})
        # 检测 2: 同一工具高频调用 (可能是暴力刷)
        tool_counts = {}
        for e in self.entries[-100:]:
            tool = e["action"].get("tool", "")
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        for tool, count in tool_counts.items():
            if count > 20:
                anomalies.append({"type": "tool_abuse", "tool": tool, "count": count})
        return anomalies
    def _hash(self, text):
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()[:12]
    def _persist(self, entry):
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    def _within_window(self, ts, target, minutes):
        # 简化: 字符串比较
        return True
if __name__ == "__main__":
    import tempfile, os
    log_path = tempfile.mktemp(suffix=".log")
    logger = SecurityAuditLogger(log_path)
    # 记录多个动作
    actions = [
        ({"tool":"search","scope":"read"}, {"risk_level":"safe"}),
        ({"tool":"delete","scope":"irreversible"}, {"risk_level":"critical"}),
        ({"tool":"update","scope":"write"}, {"risk_level":"cautious"}),
    ]
    for act, ctx in actions:
        logger.log_action(act, "用户输入", {"executed": True}, ctx)
    print(f"日志条目: {len(logger.entries)}")
    anomalies = logger.detect_anomaly()
    print(f"异常检测: {anomalies if anomalies else '无异常'}")
    trace = logger.trace_incident("2026-07-03T22:00:00", 30)
    print(f"追溯: {trace['n_actions']}动作, critical={len(trace['critical_actions'])}")
    os.unlink(log_path)

