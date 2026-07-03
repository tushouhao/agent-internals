# 最小 Agent 骨架：感知、决策、执行三步循环
# 运行: python agent.py

from typing import Any, Callable


class Agent:
    """最小 Agent 骨架：感知、决策、执行三步循环"""
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


if __name__ == "__main__":
    # 演示：简单的回声 Agent
    agent = Agent(
        perceiver=lambda obs: {"data": obs},
        decider=lambda state: f"echo_{state['data']}",
        executor=lambda action: f"executed({action})",
    )
    result = agent.step("hello")
    print(f"Agent step result: {result}")
    assert result == "executed(echo_hello)", f"Unexpected: {result}"
    print("Agent 骨架测试通过")
