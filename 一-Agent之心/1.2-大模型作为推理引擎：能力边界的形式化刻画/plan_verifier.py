# 多步规划正确性验证器
# 运行: python plan_verifier.py

class PlanVerifier:
    """多步规划的正确性验证器"""
    def __init__(self, tool_specs):
        self.tools = {t.name: t for t in tool_specs}

    def verify_plan(self, plan):
        issues = []
        for i, step in enumerate(plan):
            tool = self.tools.get(step.tool)
            if not tool:
                issues.append(f"步骤{i}: 工具{step.tool}不存在")
                continue
            # 校验输入输出对齐
            prev_outputs = set()
            for j in range(i):
                prev_outputs.update(plan[j].outputs)
            missing = set(tool.required_inputs) - prev_outputs
            if missing:
                issues.append(f"步骤{i}: 缺少必要输入{missing}")
        return issues
