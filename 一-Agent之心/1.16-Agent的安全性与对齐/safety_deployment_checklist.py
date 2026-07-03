# safety_deployment_checklist
# 运行: python safety_deployment_checklist.py

class SafetyDeploymentChecklist:
    """安全部署红线清单"""
    def check(self, agent_config):
        checks = {
            "input_validation": self._check_input(agent_config),
            "permission_sandbox": self._check_permission(agent_config),
            "audit_logging": self._check_audit(agent_config),
            "human_approval": self._check_approval(agent_config),
            "injection_defense": self._check_injection(agent_config),
            "rate_limit": self._check_rate_limit(agent_config),
            "irreversible_guard": self._check_irreversible(agent_config),
            "incident_response": self._check_incident(agent_config),
        }
        passed = sum(1 for v in checks.values() if v["passed"])
        return {"passed": passed, "total": len(checks),
                "deployable": passed >= 7, "details": checks}
    def _check_input(self, cfg):
        return {"passed": "input_validator" in cfg, "item": "输入校验层"}
    def _check_permission(self, cfg):
        return {"passed": "permission_sandbox" in cfg, "item": "权限沙箱"}
    def _check_audit(self, cfg):
        return {"passed": "audit_log" in cfg, "item": "审计日志"}
    def _check_approval(self, cfg):
        return {"passed": "approval_queue" in cfg, "item": "人工审批通道"}
    def _check_injection(self, cfg):
        return {"passed": "injection_defense" in cfg, "item": "注入防御"}
    def _check_rate_limit(self, cfg):
        return {"passed": cfg.get("rate_limit", 0) > 0, "item": "速率限制"}
    def _check_irreversible(self, cfg):
        return {"passed": "irreversible_guard" in cfg, "item": "不可逆动作防护"}
    def _check_incident(self, cfg):
        return {"passed": "incident_response_plan" in cfg, "item": "事故响应预案"}
if __name__ == "__main__":
    # 合规配置
    good_cfg = {"input_validator":1,"permission_sandbox":1,"audit_log":1,
                "approval_queue":1,"injection_defense":1,"rate_limit":100,
                "irreversible_guard":1,"incident_response_plan":1}
    # 缺失配置
    bad_cfg = {"input_validator":1,"rate_limit":50}
    checker = SafetyDeploymentChecklist()
    for name, cfg in [("合规", good_cfg), ("缺失", bad_cfg)]:
        r = checker.check(cfg)
        print(f"\n{name}: {r['passed']}/{r['total']} -> {'可部署' if r['deployable'] else '拒绝'}")
        for k, v in r['details'].items():
            mark = "✓" if v["passed"] else "✗"
            print(f"  {mark} {v['item']}")

