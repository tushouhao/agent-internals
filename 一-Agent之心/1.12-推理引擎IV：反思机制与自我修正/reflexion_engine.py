# reflexion_engine
# 运行: python reflexion_engine.py

class ReflexionEngine:
    """Reflexion 三循环引擎"""
    def __init__(self, llm, evaluator, max_iters=3):
        self.llm = llm
        self.evaluator = evaluator
        self.max_iters = max_iters
        self.reflections = []

    def solve(self, task):
        """执行-评估-反思迭代"""
        for i in range(self.max_iters):
            # 循环 1: 执行 - Actor 携带反思生成
            action = self._act(task, self.reflections)
            # 循环 2: 评估 - Evaluator 评分
            score, feedback = self.evaluator(action, task)
            if score >= 0.9:
                return action, i + 1
            # 循环 3: 反思 - Reflector 生成语言反思
            reflection = self._reflect(task, action, feedback, self.reflections)
            self.reflections.append(reflection)
        return action, self.max_iters

    def _act(self, task, reflections):
        """Actor: 携带过往反思生成行动"""
        refl_text = "\n".join(f"- {r}" for r in reflections) or "无"
        prompt = f"任务: {task}\n过往反思:\n{refl_text}\n请生成解决方案。"
        return self.llm([{"role": "user", "content": prompt}])

    def _reflect(self, task, action, feedback, prev_reflections):
        """Reflector: 语言化反思"""
        prev = "\n".join(prev_reflections) or "无"
        prompt = (f"任务: {task}\n上次尝试: {action[:200]}\n"
                  f"反馈: {feedback}\n过往反思: {prev}\n"
                  f"用一句话总结这次失败的根因和下一步改进方向。")
        return self.llm([{"role": "user", "content": prompt}])
if __name__ == "__main__":
    def llm(msgs):
        c = msgs[-1]["content"]
        if "生成" in c: return "def solve(): return 42"
        if "总结" in c: return "上次未处理边界情况, 下次加 if 判断"
        return "方案"
    def ev(action, task):
        return (0.95, "通过") if "42" in action else (0.3, "未返回预期值")
    eng = ReflexionEngine(llm, ev, max_iters=3)
    ans, iters = eng.solve("求答案")
    print(f"答案: {ans[:30]}, 迭代: {iters}次, 反思数: {len(eng.reflections)}")

