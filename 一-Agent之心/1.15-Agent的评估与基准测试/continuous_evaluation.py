# continuous_evaluation
# 运行: python continuous_evaluation.py

class ContinuousEvaluation:
    """持续评测系统"""
    def __init__(self, test_suites, alert_threshold=0.05):
        self.test_suites = test_suites
        self.alert_threshold = alert_threshold
        self.history = []

    def regression_check(self, agent, version):
        """回归评测: 与上一版本对比"""
        current = self._run_suites(agent)
        previous = self.history[-1] if self.history else None
        report = {"version": version, "scores": current,
                  "regressions": [], "improvements": []}
        if previous:
            for suite, score in current.items():
                delta = score - previous["scores"].get(suite, 0)
                if delta < -self.alert_threshold:
                    report["regressions"].append({"suite": suite, "delta": delta})
                elif delta > self.alert_threshold:
                    report["improvements"].append({"suite": suite, "delta": delta})
        self.history.append(report)
        return report

    def _run_suites(self, agent):
        return {name: self._run_suite(agent, suite)
                for name, suite in self.test_suites.items()}

    def _run_suite(self, agent, suite):
        scores = [agent.run(task)["score"] for task in suite]
        return sum(scores) / max(len(scores), 1)

    def canary_deploy(self, agent, version, traffic=0.05):
        """金丝雀部署: 小流量验证"""
        report = self.regression_check(agent, version)
        if report["regressions"]:
            return {"deploy": False, "reason": "回归超阈值",
                    "regressions": report["regressions"]}
        return {"deploy": True, "traffic": traffic, "report": report}
if __name__ == "__main__":
    suites = {"math": [{"q":"1+1","a":"2"}], "code": [{"q":"sort","a":"ok"}]}
    ce = ContinuousEvaluation(suites, alert_threshold=0.05)
    class Agent:
        def __init__(self, acc): self.acc = acc
        def run(self, task): return {"score": self.acc}
    # v1 基线
    r1 = ce.regression_check(Agent(0.8), "v1")
    print(f"v1: 数学{r1['scores']['math']:.1f} 代码{r1['scores']['code']:.1f}")
    # v2 退化
    r2 = ce.regression_check(Agent(0.7), "v2")
    print(f"v2 回归: {r2['regressions']}")
    canary = ce.canary_deploy(Agent(0.7), "v2", traffic=0.05)
    print(f"金丝雀部署: {canary['deploy']} ({canary.get('reason','通过')})")

