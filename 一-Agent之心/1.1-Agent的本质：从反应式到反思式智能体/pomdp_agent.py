# 支持部分可观测的 Agent (POMDP)
# 运行: python pomdp_agent.py

from typing import Any, Callable, Optional


class Agent:
    """基类 Agent（前置定义）"""
    def __init__(self, perceiver: Callable, decider: Callable, executor: Callable):
        self.perceiver = perceiver
        self.decider = decider
        self.executor = executor
        self.state = None

    def step(self, observation: Any) -> Any:
        self.state = self.perceiver(observation)
        action = self.decider(self.state)
        result = self.executor(action)
        return result


class POMDPAgent(Agent):
    """支持部分可观测的 Agent，带信念状态维护"""
    def __init__(self, perceiver: Callable, decider: Callable,
                 executor: Callable, belief_updater: Callable):
        super().__init__(perceiver, decider, executor)
        self.belief: Optional[dict] = None
        self.belief_updater = belief_updater

    def step(self, observation: Any) -> Any:
        self.state = self.perceiver(observation)
        self.belief = self.belief_updater(self.belief, self.state)
        action = self.decider(self.state, self.belief)
        result = self.executor(action)
        return result


if __name__ == "__main__":
    # 演示：扑克牌 belief 更新
    def simple_belief_updater(belief, state):
        if belief is None:
            return {"opponent_hand_prob": 0.5}
        return {"opponent_hand_prob": belief["opponent_hand_prob"] * 0.9}

    agent = POMDPAgent(
        perceiver=lambda obs: {"card": obs},
        decider=lambda state, belief: "call",
        executor=lambda action: f"executed_{action}",
        belief_updater=simple_belief_updater,
    )
    result = agent.step("Ace")
    print(f"POMDP result: {result}, belief: {agent.belief}")
