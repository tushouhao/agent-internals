# planner
# 运行: python planner.py

class Planner:
    """基础规划器接口"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def plan(self, goal: str, context: dict) -> list:
        """将目标分解为子目标序列"""
        raise NotImplementedError
