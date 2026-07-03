# 工具调用错误的止损策略
# 运行: python error_stop_loss.py

class ErrorStopLoss:
    """工具调用错误的止损策略"""
    def __init__(self, max_escalation_steps=2):
        self.max_escalation = max_escalation_steps
        self._failure_streak = 0

    def _consecutive_failures(self):
        return self._failure_streak

    def should_escalate(self, tool_result, step_index):
        """判断是否应该升级处理"""
        if tool_result.get("severity") == "block":
            return True  # 安全阻断，立即升级
        if tool_result.get("error"):
            self._failure_streak += 1
            if self._consecutive_failures() >= self.max_escalation:
                return True
        else:
            self._failure_streak = 0
        return False

    def escalate(self, context, tool_name):
        """升级处理：切换到确定性路径"""
        if "blocked_tools" not in context:
            context["blocked_tools"] = []
        context["mode"] = "degraded"
        context["blocked_tools"].append(tool_name)
        return f"工具 {tool_name} 暂时不可用，已切换到备用方案"

if __name__ == "__main__":
    es = ErrorStopLoss(max_escalation_steps=2)
    ctx = {"blocked_tools": []}
    # 模拟 5 步工具调用，前 3 步出错
    results = [
        {"error": "timeout"},
        {"error": "timeout"},
        {"error": "timeout"},
        {},
        {"severity": "block", "error": "safety"},
    ]
    for i, r in enumerate(results):
        if es.should_escalate(r, i):
            action = es.escalate(ctx, "search")
            print(f"步骤{i}: 升级 -> {action}")
        else:
            print(f"步骤{i}: 继续 (错误连续={es._consecutive_failures()})")
    print(f"最终上下文: {ctx}")
