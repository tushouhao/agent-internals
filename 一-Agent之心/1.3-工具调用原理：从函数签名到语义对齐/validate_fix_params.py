# 参数幻觉检测与修复
# 运行: python validate_fix_params.py

# 参数幻觉检测与修复
def validate_and_fix_parameters(call, tool_schema):
    """校验工具调用参数，尝试修复常见幻觉"""
    fixed = call.copy()
    issues = []

    # 1. 移除幻觉参数（schema 中不存在的）
    valid_params = set(tool_schema["parameters"]["properties"].keys())
    for param in list(fixed["arguments"].keys()):
        if param not in valid_params:
            issues.append(f"移除幻觉参数: {param}")
            del fixed["arguments"][param]

    # 2. 填充必填参数的默认值（如果缺失）
    required = tool_schema["parameters"].get("required", [])
    for req in required:
        if req not in fixed["arguments"]:
            default = tool_schema["parameters"]["properties"][req].get("default")
            if default is not None:
                fixed["arguments"][req] = default
                issues.append(f"填充缺失必填参数: {req}={default}")

    return fixed, issues
