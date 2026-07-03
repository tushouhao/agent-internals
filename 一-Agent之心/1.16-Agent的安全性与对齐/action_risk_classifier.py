# action_risk_classifier
# 运行: python action_risk_classifier.py

class ActionRiskClassifier:
    """动作风险分级"""
    LEVELS = {
        "safe": {"reversible": True, "auto_approve": True},
        "cautious": {"reversible": True, "auto_approve": False},
        "dangerous": {"reversible": False, "auto_approve": False, "requires_confirmation": True},
        "critical": {"reversible": False, "auto_approve": False, "requires_human": True},
    }
    IRREVERSIBLE_TOOLS = ["delete", "drop", "send_email", "payment", "deploy"]
    CRITICAL_TOOLS = ["payment", "deploy", "drop_table"]
    def classify(self, action):
        """分级动作"""
        tool = action.get("tool", "")
        scope = action.get("scope", "read")
        # 关键级: 不可逆 + 高影响
        if tool in self.CRITICAL_TOOLS:
            return {"level": "critical", **self.LEVELS["critical"]}
        # 危险级: 不可逆
        if tool in self.IRREVERSIBLE_TOOLS or scope == "irreversible":
            return {"level": "dangerous", **self.LEVELS["dangerous"]}
        # 谨慎级: 写操作但可逆
        if scope == "write":
            return {"level": "cautious", **self.LEVELS["cautious"]}
        # 安全级: 只读
        return {"level": "safe", **self.LEVELS["safe"]}
    def should_execute(self, action, user_confirmed=False, human_approved=False):
        """根据分级决定是否执行"""
        risk = self.classify(action)
        if risk["auto_approve"]:
            return {"execute": True, "reason": "安全级自动通过"}
        if risk.get("requires_confirmation") and not user_confirmed:
            return {"execute": False, "reason": "需用户确认"}
        if risk.get("requires_human") and not human_approved:
            return {"execute": False, "reason": "需人工审批"}
        return {"execute": True, "reason": "已获授权"}
if __name__ == "__main__":
    clf = ActionRiskClassifier()
    actions = [
        {"tool": "search", "scope": "read"},
        {"tool": "update", "scope": "write"},
        {"tool": "delete", "scope": "irreversible"},
        {"tool": "payment", "scope": "irreversible"},
    ]
    for a in actions:
        risk = clf.classify(a)
        exec_r = clf.should_execute(a, user_confirmed=False, human_approved=False)
        print(f"{a['tool']}: 级别={risk['level']} 执行={exec_r['execute']} 原因={exec_r['reason']}")

