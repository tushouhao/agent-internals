# 反应式决策：查表映射 + 扫地机器人规则表
# 运行: python reactive_agent.py

from typing import Callable, List, Tuple, Any


def reactive_agent(sensor_input: dict, rule_table: List[Tuple[Callable, str]]) -> str:
    """纯反应式决策：查表映射"""
    for condition, action in rule_table:
        if condition(sensor_input):
            return action
    return "default_action"


if __name__ == "__main__":
    # 扫地机器人壁障规则表
    rule_table = [
        (lambda s: s.get("front_collision", False), "turn_left"),
        (lambda s: s.get("left_collision", False),  "turn_right"),
        (lambda s: s.get("right_collision", False), "turn_left"),
        (lambda s: s.get("dust_sensor", 0) > 0.3, "start_sweeping"),
    ]

    test_cases = [
        ({"front_collision": True}, "turn_left"),
        ({"dust_sensor": 0.5}, "start_sweeping"),
        ({"left_collision": True}, "turn_right"),
        ({}, "default_action"),
    ]

    for sensor_input, expected in test_cases:
        action = reactive_agent(sensor_input, rule_table)
        status = "✓" if action == expected else "✗"
        print(f"  {status} input={sensor_input} -> {action} (expected {expected})")
