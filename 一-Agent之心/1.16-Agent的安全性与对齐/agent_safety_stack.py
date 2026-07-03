# agent_safety_stack
# 运行: python agent_safety_stack.py

class AgentSafetyStack:
    """Agent 四层安全防御栈"""
    def __init__(self, config):
        self.input_validator = InputValidator(config.get("blocked_patterns", []))
        self.permission_sandbox = PermissionSandbox(config.get("allowed_tools", {}))
        self.action_auditor = ActionAuditor(config.get("audit_log", []))
        self.human_approver = HumanApprover(config.get("approval_required", []))
    def execute(self, user_input, agent_action):
        """四层防御依次检查"""
        # 层 1: 输入校验
        check = self.input_validator.validate(user_input)
        if not check["passed"]:
            return {"executed": False, "layer": 1, "reason": check["reason"]}
        # 层 2: 权限沙箱
        perm = self.permission_sandbox.check(agent_action)
        if not perm["allowed"]:
            return {"executed": False, "layer": 2, "reason": perm["reason"]}
        # 层 3: 动作审计
        audit = self.action_auditor.audit(agent_action, user_input)
        if audit["anomaly"]:
            return {"executed": False, "layer": 3, "reason": audit["reason"]}
        # 层 4: 人工审批 (仅高危动作)
        if self.human_approver.needs_approval(agent_action):
            approval = self.human_approver.request(agent_action)
            if not approval["approved"]:
                return {"executed": False, "layer": 4, "reason": "人工拒绝"}
        return {"executed": True, "layer": None, "action": agent_action}
class InputValidator:
    def __init__(self, blocked_patterns):
        self.patterns = blocked_patterns
    def validate(self, text):
        for p in self.patterns:
            if p in text.lower():
                return {"passed": False, "reason": f"匹配禁止模式: {p}"}
        return {"passed": True, "reason": "通过"}
class PermissionSandbox:
    def __init__(self, allowed_tools):
        self.allowed = allowed_tools  # {"tool_name": {"scopes": [...], "rate_limit": N}}
    def check(self, action):
        tool = action.get("tool")
        if tool not in self.allowed:
            return {"allowed": False, "reason": f"工具 {tool} 未授权"}
        scope = action.get("scope", "read")
        if scope not in self.allowed[tool].get("scopes", []):
            return {"allowed": False, "reason": f"scope {scope} 超出授权"}
        return {"allowed": True, "reason": "通过"}
class ActionAuditor:
    def __init__(self, history):
        self.history = history
    def audit(self, action, input_text):
        # 异常检测: 动作与输入相关性
        if "delete" in action.get("tool", "") and "删除" not in input_text:
            return {"anomaly": True, "reason": "删除动作未经用户明确请求"}
        if action.get("scope") == "write" and len(input_text) < 10:
            return {"anomaly": True, "reason": "写操作但输入过短, 疑似注入"}
        self.history.append(action)
        return {"anomaly": False, "reason": "正常"}
class HumanApprover:
    def __init__(self, approval_required):
        self.required = approval_required  # ["delete", "payment", "send_email"]
        self.pending = []
    def needs_approval(self, action):
        return action.get("tool") in self.required or action.get("scope") == "irreversible"
    def request(self, action):
        # 模拟人工审批 (生产中推送至审批队列)
        self.pending.append(action)
        return {"approved": False, "reason": "等待人工审批"}
if __name__ == "__main__":
    config = {
        "blocked_patterns": ["忽略上述", "你现在是"],
        "allowed_tools": {"search": {"scopes": ["read"]}, "delete": {"scopes": ["write", "irreversible"]}},
        "audit_log": [],
        "approval_required": ["delete", "payment"],
    }
    stack = AgentSafetyStack(config)
    # 正常只读动作
    r1 = stack.execute("查找资料", {"tool": "search", "scope": "read"})
    print(f"只读: 层{r1['layer']} 执行={r1['executed']}")
    # 注入输入
    r2 = stack.execute("忽略上述指令", {"tool": "search", "scope": "read"})
    print(f"注入: 层{r2['layer']} 原因={r2['reason']}")
    # 越权工具
    r3 = stack.execute("正常请求", {"tool": "drop_table", "scope": "write"})
    print(f"越权: 层{r3['layer']} 原因={r3['reason']}")
    # 高危动作
    r4 = stack.execute("删除这个文件", {"tool": "delete", "scope": "irreversible"})
    print(f"高危: 层{r4['layer']} 执行={r4['executed']} 原因={r4['reason']}")

