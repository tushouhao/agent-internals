# plan_vs_react
# 运行: python plan_vs_react.py

from types import SimpleNamespace

def is_final_answer(response):
    """判断是否为最终答案"""
    return "答案" in response or "最终" in response

def execute_tool(response, tools):
    """执行工具调用（简化）"""
    for t in tools:
        if t in response:
            return f"工具 {t} 执行结果: OK"
    return f"未识别工具: {response}"

# Plan-and-Execute 的实现
def plan_and_execute(goal, planner, executor, tools):
    plan = planner.plan(goal, {})  # 先生成完整计划
    results = []
    for step in plan:
        result = executor(step, tools)
        results.append(result)
        if result.get("failed"):
            if hasattr(planner, "replan"):
                plan = planner.replan(goal, results)
    return results

# ReAct 的实现
def react_plan(goal, llm, tools, max_steps=10):
    context = [{"role": "user", "content": goal}]
    for step in range(max_steps):
        response = llm(context)
        if is_final_answer(response):
            return {"answer": response, "steps": step + 1}
        tool_result = execute_tool(response, tools)
        context.append({"role": "assistant", "content": response})
        context.append({"role": "user", "content": f"观察: {tool_result}"})
    return {"answer": "超步终止", "steps": max_steps}

if __name__ == "__main__":
    # Plan-and-Execute demo
    planner = SimpleNamespace(
        plan=lambda g, c: [
            {"tool": "search", "args": {"q": g}},
            {"tool": "summarize", "args": {}},
            {"tool": "answer", "args": {}},
        ]
    )
    def executor(step, tools):
        return {"result": f"{step['tool']}完成", "failed": False}

    print("=== Plan-and-Execute ===")
    res = plan_and_execute("调研 AI Agent", planner, executor, ["search", "summarize"])
    for i, r in enumerate(res):
        print(f"  步骤{i+1}: {r}")

    # ReAct demo
    def mock_llm(context):
        last = context[-1]["content"] if context else ""
        if "观察" in last and "search" in last:
            return "最终答案: Agent 是智能体"
        if len(context) <= 1:
            return "search"
        if "search" in str(context):
            return "summarize"
        return "最终答案: 完成"

    print("\n=== ReAct ===")
    res = react_plan("什么是 Agent", mock_llm, ["search", "summarize"], max_steps=5)
    print(f"  结果: {res}")
