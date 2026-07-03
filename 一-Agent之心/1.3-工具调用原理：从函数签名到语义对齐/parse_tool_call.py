# 工具调用解析器
# 运行: python parse_tool_call.py

def parse_tool_call(llm_output: str, tool_schemas: dict) -> dict:
    """解析 LLM 输出中的工具调用，返回结构化调用"""
    import json
    try:
        call = json.loads(llm_output)
    except json.JSONDecodeError:
        # 尝试提取 JSON 片段
        start = llm_output.find('{')
        end = llm_output.rfind('}') + 1
        if start >= 0 and end > start:
            call = json.loads(llm_output[start:end])
        else:
            raise ValueError("无法解析工具调用")
    # 校验工具是否存在
    if call.get("name") not in tool_schemas:
        raise ValueError(f"未知工具: {call.get('name')}")
    return call
