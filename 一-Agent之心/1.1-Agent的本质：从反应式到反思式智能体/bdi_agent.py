# BDI 模型最小骨架（Belief-Desire-Intention）
# 运行: python bdi_agent.py

from typing import List, Set, Dict, Any


class BDIAgent:
    """BDI 模型最小骨架"""
    def __init__(self):
        self.beliefs: Set[str] = set()
        self.desires: List[str] = []
        self.intentions: List[str] = []
        self.plans: Dict[str, List[str]] = {}

    def update_beliefs(self, percept: List[str]) -> None:
        self.beliefs.update(percept)

    def _generate_options(self) -> List[str]:
        """根据当前信念生成候选愿望"""
        if "urgent_order" in self.beliefs:
            return ["approve_urgent", "flag_review"]
        return ["auto_approve", "manual_review", "reject"]

    def _filter_by_beliefs(self, options: List[str]) -> List[str]:
        """根据信念过滤不可行的愿望"""
        filtered = []
        for opt in options:
            if opt == "approve_urgent" and "high_risk" in self.beliefs:
                continue
            filtered.append(opt)
        return filtered

    def deliberate(self) -> None:
        self.desires = self._generate_options()
        self.intentions = self._filter_by_beliefs(self.desires)

    def _plan_first_intention(self) -> List[str]:
        """为第一个意图生成行动计划"""
        if not self.intentions:
            return []
        intent = self.intentions[0]
        return self.plans.get(intent, [f"execute_{intent}"])

    def execute_intention(self) -> List[Any]:
        self.deliberate()
        results = []
        for action in self._plan_first_intention():
            result = f"action({action}) executed"
            results.append(result)
            self.update_beliefs([result])
        return results


if __name__ == "__main__":
    agent = BDIAgent()
    agent.plans = {"manual_review": ["check_docs", "verify_amount", "approve"]}
    agent.update_beliefs(["urgent_order"])

    results = agent.execute_intention()
    print(f"BDI 执行结果: {results}")
    print(f"最终信念: {agent.beliefs}")
