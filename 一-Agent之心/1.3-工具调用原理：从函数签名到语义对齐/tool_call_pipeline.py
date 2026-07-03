# 生产级工具调用管线
# 运行: python tool_call_pipeline.py

import json, re

class TemporaryError(Exception):
    """临时性错误（可重试）"""
    pass

def validate_and_fix_parameters(call, schema):
    """参数修复（简化版）"""
    fixed = call.copy()
    if "arguments" not in fixed:
        fixed["arguments"] = {}
    issues = []
    valid_params = set(schema.get("params", {}).keys())
    for p in list(fixed["arguments"].keys()):
        if p not in valid_params:
            issues.append(f"移除幻觉参数: {p}")
            del fixed["arguments"][p]
    return fixed, issues

class ToolCallPipeline:
    """生产级工具调用管线"""
    def __init__(self, tool_registry, max_retries=2):
        self.registry = tool_registry
        self.max_retries = max_retries

    def _parse(self, llm_output):
        """阶段1: 解析 LLM 输出为工具调用"""
        m = re.search(r'(\w+)\s+(\{[^}]*\})', llm_output)
        if not m:
            start = llm_output.find('{')
            end = llm_output.rfind('}') + 1
            if start >= 0 and end > start:
                args = json.loads(llm_output[start:end])
                return {"name": next(iter(self.registry.schemas)), "arguments": args}
            raise ValueError("无法解析")
        return {"name": m.group(1), "arguments": json.loads(m.group(2))}

    def _validate_schema(self, call, schema):
        violations = []
        valid_params = set(schema.get("params", {}).keys())
        for p in call["arguments"]:
            if p not in valid_params:
                violations.append(f"参数 {p} 不在 schema")
        return violations

    def _handle_schema_violations(self, violations, call, context):
        return {"error": "schema_violation", "violations": violations}

    def _log_fixes(self, fixes):
        print(f"  [log] 参数修复: {fixes}")

    def _safety_check(self, call, context):
        # 简化: 非破坏性工具一律通过
        return call["name"] != "drop_table"

    def _sanitize_result(self, result):
        return {"result": str(result)[:200], "sanitized": True}

    def process(self, llm_output, context):
        call = self._parse(llm_output)
        if call["name"] not in self.registry.schemas:
            return {"error": f"未知工具 {call['name']}", "severity": "block"}
        schema = self.registry.get_schema(call["name"])
        violations = self._validate_schema(call, schema)
        if violations:
            return self._handle_schema_violations(violations, call, context)
        call, fixes = validate_and_fix_parameters(call, schema)
        if fixes:
            self._log_fixes(fixes)
        if not self._safety_check(call, context):
            return {"error": "安全策略拒绝", "severity": "block"}
        result = None
        for attempt in range(self.max_retries + 1):
            try:
                result = self.registry.execute(call)
                return {"result": result, "call": call}
            except TemporaryError as e:
                if attempt < self.max_retries:
                    continue
                return {"error": str(e), "severity": "temporary"}
        return self._sanitize_result(result)

if __name__ == "__main__":
    class MockRegistry:
        schemas = {"get_weather": {"params": {"city": "string"}},
                   "send_email": {"params": {"to": "string", "body": "string"}}}
        def get_schema(self, n):
            return self.schemas.get(n, {"params": {}})
        def execute(self, call):
            return f"执行 {call['name']} 参数={call['arguments']}"

    pipe = ToolCallPipeline(MockRegistry(), max_retries=2)
    cases = [
        '调用 get_weather {"city": "Beijing"}',
        'send_email {"to": "a@b.com", "body": "hi", "extra": 1}',
        'drop_table {"name": "users"}',
    ]
    for c in cases:
        print(f"\n输入: {c}")
        r = pipe.process(c, {})
        print(f"  结果: {r}")
