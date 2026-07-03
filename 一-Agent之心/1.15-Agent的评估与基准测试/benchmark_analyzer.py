# benchmark_analyzer
# 运行: python benchmark_analyzer.py

class BenchmarkAnalyzer:
    """基准分析器"""
    def __init__(self):
        self.benchmarks = {
            "AgentBench": {"domains": 8, "tasks": 200, "interactive": True,
                           "metric": "success_rate", "env": "sandbox"},
            "WebArena": {"domains": 4, "tasks": 812, "interactive": True,
                         "metric": "end_state_match", "env": "real_web"},
            "SWE-bench": {"domains": 1, "tasks": 2298, "interactive": False,
                          "metric": "test_pass", "env": "code_repo"},
        }

    def analyze(self, name):
        b = self.benchmarks[name]
        tradeoffs = {
            "strength": self._strength(b),
            "blind_spot": self._blind_spot(b),
            "gaming_risk": self._gaming_risk(b),
        }
        return {"config": b, **tradeoffs}

    def _strength(self, b):
        if b["interactive"]: return "评估真实交互能力"
        if b["domains"] > 1: return "跨领域覆盖广"
        return "深度评估单一领域"

    def _blind_spot(self, b):
        blind = []
        if not b["interactive"]: blind.append("忽略交互失败恢复")
        if b["domains"] == 1: blind.append("单领域无法泛化")
        if b["env"] == "sandbox": blind.append("与真实环境差距")
        return blind

    def _gaming_risk(self, b):
        risks = []
        if b["metric"] == "test_pass": risks.append("刷测试用例而非真修复")
        if b["metric"] == "end_state_match": risks.append("暴力路径达终态")
        if b["domains"] > 4: risks.append("选简单领域刷分")
        return risks
if __name__ == "__main__":
    ba = BenchmarkAnalyzer()
    for name in ["AgentBench", "WebArena", "SWE-bench"]:
        r = ba.analyze(name)
        print(f"\n{name}:")
        print(f"  优势: {r['strength']}")
        print(f"  盲区: {r['blind_spot']}")
        print(f"  刷榜风险: {r['gaming_risk']}")

