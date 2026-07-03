# 工具调用解析器
# 运行: python parse_tool_call.py

import json

def parse_tool_call(llm_output: str, tool_schemas: dict) -> dict:
    """解析 LLM 输出中的工具调用，返回结构化调用。
    支持两种格式: 直接 JSON 或 '调用 tool_name {"args":...}' 嵌入式。
    """
    # 先尝试整体解析
    try:
        call = json.loads(llm_output)
        if call.get("name") in tool_schemas:
            return call
    except json.JSONDecodeError:
        pass

    # 尝试提取工具名 + JSON 片段
    import re
    m = re.search(r'(\w+)\s+(\{[^}]*\})', llm_output)
    if not m:
        # 仅提取 JSON 片段，工具名从外部推断
        start = llm_output.find('{')
        end = llm_output.rfind('}') + 1
        if start >= 0 and end > start:
            args = json.loads(llm_output[start:end])
            # 从 schemas 中匹配第一个
            for name in tool_schemas:
                if name in llm_output:
                    return {"name": name, "arguments": args}
            raise ValueError(f"未知工具: None")
        raise ValueError("无法解析工具调用")

    name, args_str = m.group(1), m.group(2)
    if name not in tool_schemas:
        raise ValueError(f"未知工具: {name}")
    return {"name": name, "arguments": json.loads(args_str)}

if __name__ == "__main__":
    schemas = {"get_weather": {"params": {"city": "string"}},
               "send_email": {"params": {"to": "string", "body": "string"}}}

    cases = [
        '{"name": "get_weather", "arguments": {"city": "Beijing"}}',
        '我要查天气，调用 get_weather {"city": "Shanghai"}',
        '请发邮件 send_email {"to": "a@b.com", "body": "hello"}',
    ]
    for c in cases:
        try:
            call = parse_tool_call(c, schemas)
            print(f"输入: {c}")
            print(f"  解析: {call}")
        except ValueError as e:
            print(f"输入: {c}\n  错误: {e}")
