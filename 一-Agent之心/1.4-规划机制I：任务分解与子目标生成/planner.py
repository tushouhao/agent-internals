# planner
# 运行: python planner.py

class Planner:
    """基础规划器：将目标分解为子目标序列"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def plan(self, goal: str, context: dict) -> list:
        """将目标分解为子目标序列。
        调用 LLM 生成计划文本，解析为步骤列表。
        """
        prompt = f"目标: {goal}\n可用工具: {', '.join(self.tools)}\n请分解为步骤。"
        plan_text = self.llm(prompt)
        return self._parse_plan(plan_text)

    def _parse_plan(self, plan_text):
        """解析 LLM 返回的计划文本为步骤列表"""
        steps = []
        for line in plan_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            # 去除序号前缀
            import re
            cleaned = re.sub(r'^\d+[\.\、\)]\s*', '', line)
            # 匹配工具
            for t in self.tools:
                if t in cleaned:
                    steps.append({"tool": t, "description": cleaned})
                    break
            else:
                if cleaned:
                    steps.append({"tool": "reasoning", "description": cleaned})
        return steps

if __name__ == "__main__":
    def mock_llm(prompt):
        return """1. search 搜索相关资料
2. summarize 总结要点
3. send 发送报告"""

    planner = Planner(mock_llm, tools=["search", "summarize", "send"])
    plan = planner.plan("调研 AI Agent 并汇报", {})
    print(f"目标: 调研 AI Agent 并汇报")
    print(f"计划 ({len(plan)} 步):")
    for i, step in enumerate(plan):
        print(f"  {i+1}. [{step['tool']}] {step['description']}")
