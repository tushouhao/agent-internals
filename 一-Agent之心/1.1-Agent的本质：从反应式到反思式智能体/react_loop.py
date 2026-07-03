# ReAct 循环的工程实现
# 运行: python react_loop.py

from typing import Optional, Any


class ToolCall:
    """模拟工具调用结果"""
    def __init__(self, name: str, args: dict):
        self.name = name
        self.args = args


def parse_tool_call(response: str) -> Optional[ToolCall]:
    """解析 LLM 输出中的工具调用（模拟实现）"""
    if "SEARCH:" in response:
        query = response.split("SEARCH:")[1].strip()
        return ToolCall("search", {"query": query})
    if "CALC:" in response:
        expr = response.split("CALC:")[1].strip()
        return ToolCall("calculate", {"expression": expr})
    return None


def react_loop(prompt: str, llm, tools: dict, max_steps: int = 10) -> str:
    """ReAct 循环：思考-行动-观察"""
    messages = [{"role": "user", "content": prompt}]
    for step in range(max_steps):
        response = llm(messages)
        action = parse_tool_call(response)
        if action is None:
            return response
        observation = tools[action.name](**action.args)
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": f"观察: {observation}"})
    return "超步终止"


if __name__ == "__main__":
    # 模拟 LLM
    def mock_llm(messages):
        last = messages[-1]["content"]
        if "观察" in last:
            return "task_complete"
        return "SEARCH: weather_beijing"

    # 模拟工具
    tools = {
        "search": lambda query: f"结果: {query} 的数据已找到",
        "calculate": lambda expression: f"结果: {eval(expression)}",
    }

    result = react_loop("北京的天气如何？", mock_llm, tools)
    print(f"ReAct 执行结果: {result}")
