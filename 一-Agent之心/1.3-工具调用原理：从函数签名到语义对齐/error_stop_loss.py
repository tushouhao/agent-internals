# 工具调用错误的止损策略
# 运行: python error_stop_loss.py

class ErrorStopLoss:
    """工具调用错误的止损策略"""
    def __init__(self, max_escalation_steps=2):
        self.max_escalation = max_escalation_steps

    def should_escalate(self, tool_result, step_index):
        """判断是否应该升级处理"""
        if tool_result.get("severity") == "block":
            return True  # 安全阻断，立即升级
        if tool_result.get("error"):
            # 连续失败时升级
            if self._consecutive_failures() >= self.max_escalation:
                return True
        return False

    def escalate(self, context, tool_name):
        """升级处理：切换到确定性路径"""
        context["mode"] = "degraded"
        context["blocked_tools"].append(tool_name)
        return f"工具 {tool_name} 暂时不可用，已切换到备用方案"
