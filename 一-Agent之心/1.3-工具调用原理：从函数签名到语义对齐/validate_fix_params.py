# 参数幻觉检测与修复
# 运行: python validate_fix_params.py

def validate_and_fix_parameters(call, tool_schema):
    """校验工具调用参数，尝试修复常见幻觉。
    schema 格式: {"parameters": {"properties": {...}, "required": [...]}}
    call 格式: {"name": ..., "arguments": {...}}
    """
    fixed = call.copy()
    fixed["arguments"] = dict(call.get("arguments", {}))
    issues = []

    valid_params = set(tool_schema["parameters"]["properties"].keys())
    # 1. 移除幻觉参数
    for param in list(fixed["arguments"].keys()):
        if param not in valid_params:
            issues.append(f"移除幻觉参数: {param}")
            del fixed["arguments"][param]

    # 2. 填充缺失必填参数的默认值
    required = tool_schema["parameters"].get("required", [])
    for req in required:
        if req not in fixed["arguments"]:
            spec = tool_schema["parameters"]["properties"].get(req, {})
            default = spec.get("default")
            if default is not None:
                fixed["arguments"][req] = default
                issues.append(f"填充缺失必填参数: {req}={default}")
            else:
                issues.append(f"⚠ 缺失必填参数且无默认值: {req}")

    # 3. 类型修复（字符串数字转 int）
    for p, spec in tool_schema["parameters"]["properties"].items():
        if p in fixed["arguments"] and spec.get("type") == "integer":
            v = fixed["arguments"][p]
            if isinstance(v, str) and v.isdigit():
                fixed["arguments"][p] = int(v)
                issues.append(f"类型修复: {p} '{v}' -> {int(v)}")

    return fixed, issues

if __name__ == "__main__":
    schema = {"parameters": {
        "properties": {
            "city": {"type": "string"},
            "days": {"type": "integer", "default": 1},
        },
        "required": ["city"],
    }}
    call = {"name": "get_weather",
             "arguments": {"city": "Beijing", "days": "3", "unit": "celsius"}}
    fixed, fixes = validate_and_fix_parameters(call, schema)
    print(f"原始调用: {call['arguments']}")
    print(f"修复后:   {fixed['arguments']}")
    print(f"修复记录 ({len(fixes)} 项):")
    for f in fixes:
        print(f"  - {f}")
