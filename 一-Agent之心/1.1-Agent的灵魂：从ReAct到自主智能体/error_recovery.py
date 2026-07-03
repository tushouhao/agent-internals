# error_recovery
# 运行: python error_recovery.py

class ErrorRecovery:
    """Agent 错误恢复机制"""
    def __init__(self, max_retries=3, fallback_strategy="retry"):
        self.max_retries = max_retries
        self.fallback = fallback_strategy
        self.error_log = []

    def with_recovery(self, action, context):
        """带错误恢复的执行"""
        for attempt in range(self.max_retries):
            try:
                result = action(context)
                return {"success": True, "result": result, "attempts": attempt + 1}
            except Exception as e:
                self.error_log.append({"error": str(e), "attempt": attempt})
                # 策略 1: 重试 (相同输入)
                if self.fallback == "retry": continue
                # 策略 2: 降级 (简化输入)
                if self.fallback == "degrade":
                    context = self._simplify(context)
                # 策略 3: 回退 (返回上一步)
                if self.fallback == "rollback":
                    return {"success": False, "rollback": True, "error": str(e)}
        # 所有重试失败
        return {"success": False, "error": self.error_log[-1]["error"], "attempts": self.max_retries}

    def _simplify(self, context):
        """降级: 简化上下文"""
        if isinstance(context, str): return context[:500]
        return context

    def spiral_detection(self, trajectory, window=3):
        """检测循环卡死: 重复相同动作"""
        actions = [t.get("action", "") for t in trajectory if "action" in t]
        for i in range(len(actions) - window + 1):
            if len(set(actions[i:i+window])) == 1:
                return {"spiral": True, "action": actions[i], "start": i}
        return {"spiral": False}
if __name__ == "__main__":
    er = ErrorRecovery(max_retries=3, fallback_strategy="retry")
    attempt_count = [0]
    def flaky_action(ctx):
        attempt_count[0] += 1
        if attempt_count[0] < 2: raise Exception("瞬时错误")
        return "成功"
    r1 = er.with_recovery(flaky_action, "输入")
    print(f"瞬时错误恢复: {r1['success']}, 尝试{r1['attempts']}次")
    def always_fail(ctx): raise Exception("永久错误")
    r2 = er.with_recovery(always_fail, "输入")
    print(f"永久错误: {r2['success']}, 尝试{r2['attempts']}次")
    traj = [{"action":"search"},{"action":"search"},{"action":"search"},{"action":"calc"}]
    spiral = er.spiral_detection(traj, window=3)
    print(f"螺旋检测: {spiral}")

