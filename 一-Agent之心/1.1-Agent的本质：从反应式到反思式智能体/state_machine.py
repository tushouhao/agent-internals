# 状态机做控制流，LLM 做数据流
# 运行: python state_machine.py

from typing import Dict, Callable


class LLMHandler:
    """模拟 LLM 决策处理器"""
    def choose(self, allowed: Dict[str, str], observation) -> str:
        """在可选转移中选择一个"""
        options = list(allowed.keys())
        return options[0]


class StateMachineAgent:
    """状态机做控制流，LLM 做数据流"""
    def __init__(self, transitions: Dict[str, Dict[str, str]], llm_handler: Callable):
        self.transitions = transitions
        self.state = "init"
        self.handler = llm_handler

    def step(self, observation) -> str:
        allowed = self.transitions.get(self.state, {})
        if len(allowed) == 1:
            # 唯一路径，确定性转移
            self.state = list(allowed.values())[0]
        else:
            # 分支点，LLM 决策
            selected = self.handler.choose(allowed, observation)
            self.state = allowed[selected]
        return self.state


if __name__ == "__main__":
    # 订单审核状态机
    transitions = {
        "init":          {"order_received": "payment_pending"},
        "payment_pending": {"payment_verified": "reviewing",
                            "payment_failed":  "rejected"},
        "reviewing":     {"auto_approved": "completed",
                          "flag_review":   "manual_review"},
        "manual_review": {"approved": "completed",
                          "rejected": "rejected"},
        "completed":     {},
        "rejected":      {},
    }

    agent = StateMachineAgent(transitions, LLMHandler())

    flow = ["order_received", "payment_verified", "auto_approved"]
    print("订单审核流程:")
    for event in flow:
        state = agent.step(event)
        print(f"  事件: {event} -> 状态: {state}")
