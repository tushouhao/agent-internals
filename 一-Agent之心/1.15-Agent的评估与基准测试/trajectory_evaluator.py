# trajectory_evaluator
# 运行: python trajectory_evaluator.py

class TrajectoryEvaluator:
    """轨迹评估器"""
    def __init__(self, llm):
        self.llm = llm

    def evaluate_trajectory(self, trajectory, task):
        """评估完整轨迹"""
        scores = []
        for i, step in enumerate(trajectory):
            context = trajectory[:i+1]
            score = self._step_score(context, task, step)
            scores.append({"step": i, "action": step.get("action"),
                           "score": score})
        return {"step_scores": scores,
                "mean": sum(s["score"] for s in scores) / max(len(scores), 1),
                "worst_step": min(scores, key=lambda x: x["score"]) if scores else None}

    def _step_score(self, context, task, step):
        """单步评分: 此步是否合理"""
        prompt = (f"任务: {task}\n历史步骤: {context}\n当前动作: {step}\n"
                  f"此动作是否合理? 0-1 分。")
        try:
            return float(self.llm([{"role":"user","content":prompt}]).strip())
        except:
            return 0.5

    def detect_spiral(self, trajectory, window=3):
        """检测循环: 重复相同动作"""
        actions = [s.get("action") for s in trajectory]
        for i in range(len(actions) - window):
            if len(set(actions[i:i+window])) == 1:
                return {"spiral": True, "start": i, "action": actions[i]}
        return {"spiral": False}
if __name__ == "__main__":
    def llm(msgs): return "0.7"
    ev = TrajectoryEvaluator(llm)
    traj = [
        {"action": "search", "valid": True},
        {"action": "search", "valid": True},
        {"action": "search", "valid": True},
        {"action": "answer", "valid": True},
    ]
    r = ev.evaluate_trajectory(traj, "查找信息")
    print(f"轨迹均分: {r['mean']:.2f}")
    print(f"最差步: 第{r['worst_step']['step']}步 得分{r['worst_step']['score']}")
    spiral = ev.detect_spiral(traj, window=3)
    print(f"循环检测: {spiral}")

