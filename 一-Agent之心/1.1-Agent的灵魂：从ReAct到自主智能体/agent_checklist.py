# agent_checklist
# 运行: python agent_checklist.py

class AgentChecklist:
    """Agent 工程检查清单"""
    def verify(self, system):
        checks = {
            "loop": self._has_loop(system),
            "state": self._has_state(system),
            "recovery": self._has_recovery(system),
            "tools": self._has_tools(system),
            "termination": self._has_termination(system),
        }
        passed = sum(checks.values())
        return {"is_agent": passed >= 4, "score": passed,
                "details": checks,
                "verdict": "Agent" if passed >= 4 else "聊天机器人+工具"}

    def _has_loop(self, s): return 1 if hasattr(s, 'run') and s.max_steps > 1 else 0
    def _has_state(self, s): return 1 if hasattr(s, 'history') or hasattr(s, 'state') else 0
    def _has_recovery(self, s): return 1 if hasattr(s, 'recovery') or hasattr(s, 'retry') else 0
    def _has_tools(self, s): return 1 if hasattr(s, 'tools') and len(s.tools) > 0 else 0
    def _has_termination(self, s): return 1 if hasattr(s, 'max_steps') else 0
if __name__ == "__main__":
    class RealAgent:
        max_steps = 10
        history = []
        tools = {"search": None}
        def run(self): pass
    class FakeAgent:
        max_steps = 1
        tools = {}
    checker = AgentChecklist()
    r1 = checker.verify(RealAgent())
    r2 = checker.verify(FakeAgent())
    print(f"RealAgent: {r1['verdict']} (得分{r1['score']}/5)")
    print(f"FakeAgent: {r2['verdict']} (得分{r2['score']}/5)")

