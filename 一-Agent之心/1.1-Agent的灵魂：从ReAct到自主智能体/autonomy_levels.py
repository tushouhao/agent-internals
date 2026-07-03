# autonomy_levels
# 运行: python autonomy_levels.py

class AutonomyLevels:
    """Agent 自主性三级"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def reactive(self, input_text):
        """一级 反应式: 直接响应, 无规划"""
        return self.llm([{"role": "user", "content": input_text}])

    def deliberative(self, input_text):
        """二级 审议式: 先规划再执行"""
        # 步骤 1: 规划
        plan = self.llm([{"role": "user", "content": f"规划任务步骤: {input_text}"}])
        steps = [s.strip() for s in plan.split("\n") if s.strip()][:5]
        # 步骤 2: 逐步执行
        results = []
        for step in steps:
            result = self.llm([{"role": "user", "content": f"执行: {step}"}])
            results.append(result)
        return {"plan": steps, "results": results}

    def reflective(self, input_text, max_iters=3):
        """三级 反思式: 执行后自评修正"""
        for i in range(max_iters):
            # 执行
            result = self.deliberative(input_text)
            # 自评
            eval_prompt = f"任务: {input_text}\n结果: {result['results']}\n结果是否正确? 有何缺陷?"
            evaluation = self.llm([{"role": "user", "content": eval_prompt}])
            if "正确" in evaluation and "缺陷" not in evaluation:
                return {"result": result, "iterations": i + 1, "passed": True}
            # 修正
            input_text = f"{input_text}\n上次缺陷: {evaluation}\n请修正。"
        return {"result": result, "iterations": max_iters, "passed": False}
if __name__ == "__main__":
    def llm(msgs):
        c = msgs[-1]["content"]
        if "规划" in c: return "1. 搜索\n2. 计算\n3. 总结"
        if "执行" in c: return "完成该步骤"
        if "是否正确" in c: return "结果正确, 无缺陷"
        return "结果"
    al = AutonomyLevels(llm, {})
    print(f"反应式: {al.reactive('问题')[:30]}")
    r2 = al.deliberative("完成任务")
    print(f"审议式: {len(r2['plan'])}步计划")
    r3 = al.reflective("高价值任务")
    print(f"反思式: 迭代{r3['iterations']}次, 通过={r3['passed']}")

