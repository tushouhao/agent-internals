# depth_controller
# 运行: python depth_controller.py

class ReasoningDepthController:
    """推理深度控制器"""
    def __init__(self, max_depth=8, drift_threshold=0.15):
        self.max_depth = max_depth
        self.drift_threshold = drift_threshold

    def should_continue(self, step, reasoning_chain):
        """判断是否应继续推理"""
        if step >= self.max_depth:
            return False, "max_depth"

        drift = self._measure_drift(reasoning_chain)
        if drift > self.drift_threshold and step > 3:
            return False, f"drift_{drift:.2f}"

        if step >= 3:
            convergence = self._measure_convergence(reasoning_chain[-3:])
            if convergence > 0.85:
                return False, f"converged_{convergence:.2f}"

        return True, "continue"

    def _measure_drift(self, chain):
        """测量推理链相对初始目标的漂移"""
        if len(chain) < 2:
            return 0.0
        first, last = chain[0], chain[-1]
        w1, w2 = set(first.split()), set(last.split())
        return 1 - len(w1 & w2) / max(len(w1 | w2), 1)

    def _measure_convergence(self, recent_steps):
        """测量最近步骤的收敛度"""
        if len(recent_steps) < 2:
            return 0.0
        sims = []
        for i in range(len(recent_steps) - 1):
            w1, w2 = set(recent_steps[i].split()), set(recent_steps[i+1].split())
            sims.append(len(w1 & w2) / max(len(w1 | w2), 1))
        return sum(sims) / len(sims)
if __name__ == "__main__":
    dc = ReasoningDepthController(max_depth=8)
    chain = ["理解问题 求2+2","识别 加法","计算 2+2=4","验证 4正确","确认 4","输出 4","重复 4","重复 4"]
    for s in range(len(chain)):
        cont, reason = dc.should_continue(s, chain[:s+1])
        if not cont: print(f"步{s}: 停止 {reason}"); break
    else: print("全部继续")
