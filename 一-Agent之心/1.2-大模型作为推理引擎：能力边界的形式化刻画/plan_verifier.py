# 多步规划正确性验证器
# 运行: python plan_verifier.py

from types import SimpleNamespace

class PlanVerifier:
    """多步规划的正确性验证器"""
    def __init__(self, tool_specs):
        # tool_specs 是工具对象列表，每个有 .name 和 .required_inputs
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

if __name__ == "__main__":
    # 构造工具规格
    search = SimpleNamespace(name="search", required_inputs=["query"])
    send_email = SimpleNamespace(name="send_email", required_inputs=["to", "body"])
    verifier = PlanVerifier([search, send_email])

    # 构造计划（第二步缺少 body 输入）
    plan = [
        SimpleNamespace(tool="search", outputs=["query"], args={"query": "AI Agent"}),
        SimpleNamespace(tool="send_email", outputs=[], args={"to": "user@example.com"}),
    ]
    issues = verifier.verify_plan(plan)
    print(f"计划验证发现 {len(issues)} 个问题:")
    for iss in issues:
        print(f"  - {iss}")
