# 生产级工具调用管线
# 运行: python tool_call_pipeline.py

class ToolCallPipeline:
    """生产级工具调用管线"""
    def __init__(self, tool_registry, max_retries=2):
        self.registry = tool_registry
        self.max_retries = max_retries

    def process(self, llm_output, context):
        # 阶段 1: 解析
        call = self._parse(llm_output)

        # 阶段 2: Schema 校验
        schema = self.registry.get_schema(call["name"])
        violations = self._validate_schema(call, schema)
        if violations:
            return self._handle_schema_violations(violations, call, context)

        # 阶段 3: 参数修复
        call, fixes = validate_and_fix_parameters(call, schema)
        if fixes:
            self._log_fixes(fixes)

        # 阶段 4: 安全检查
        if not self._safety_check(call, context):
            return {"error": "安全策略拒绝", "severity": "block"}

        # 阶段 5: 执行 + 重试
        for attempt in range(self.max_retries + 1):
            try:
                result = self.registry.execute(call)
                return {"result": result, "call": call}
            except TemporaryError as e:
                if attempt < self.max_retries:
                    continue
                return {"error": str(e), "severity": "temporary"}

        # 阶段 6: 结果回灌（清洗）
        return self._sanitize_result(result)
