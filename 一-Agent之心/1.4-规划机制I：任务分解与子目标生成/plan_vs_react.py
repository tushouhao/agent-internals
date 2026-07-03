# plan_vs_react
# 运行: python plan_vs_react.py

# Plan-and-Execute 的实现
def plan_and_execute(goal, planner, executor, tools):
    plan = planner.plan(goal)  # 先生成完整计划
    results = []
    for step in plan:
        result = executor(step, tools)
        results.append(result)
        # 不重新规划，除非遇到失败
        if result.get("failed"):
            plan = planner.replan(goal, results)
    return results

# ReAct 的实现
def react_plan(goal, llm, tools, max_steps=10):
    context = [{"role": "user", "content": goal}]
    for step in range(max_steps):
        response = llm(context)
        if is_final_answer(response):
            return response
        tool_result = execute_tool(response, tools)
        context.append({"role": "assistant", "content": response})
        context.append({"role": "user", "content": f"观察: {tool_result}"})
    return "超步终止"
