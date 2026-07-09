# 文件名: window_exhaust.py
# 功能: 多轮对话累积 token 耗尽窗口止于检测缺失致拒答率 100%
# 运行: python window_exhaust.py

"""窗口耗尽阶：多轮累积 token，崩在检测漏。"""

import random

random.seed(42)


def mock_multi_turn_accumulate(turn: int, inject_exhaust: bool = False) -> dict:
    if inject_exhaust:
        return {"turn": turn, "tokens": 8192 + turn * 100, "exhausted": True}
    return {"turn": turn, "tokens": turn * 100, "exhausted": False}


def detect_window(tokens: int, window_limit: int = 8192) -> bool:
    return tokens > window_limit


def run_window_exhaust(turn: int) -> dict:
    r = mock_multi_turn_accumulate(turn, inject_exhaust=random.random() < 1.0)
    if not detect_window(r["tokens"]):
        return {"answered": True, "reason": "窗口充裕", "exhausted": False}
    return {"answered": False, "reason": "窗口耗尽", "exhausted": True}


def simulate_exhaust(n: int = 50) -> dict:
    answered = 0
    exhausted = 0
    for i in range(n):
        r = run_window_exhaust(i)
        if r["answered"]:
            answered += 1
        else:
            exhausted += 1
    return {"answered_rate": answered / n, "exhausted_rate": exhausted / n, "n": n}


def main():
    r = simulate_exhaust(50)
    print("窗口耗尽阶仿真结果（n=50）:")
    print(f"  拒答率: {(1 - r['answered_rate']):.0%}（窗口耗尽即弃）")
    print(f"  耗尽率: {r['exhausted_rate']:.0%}（多轮累积 token 超窗口）")
    print(f"  崩溃模式: 检测漏——窗口耗尽无检测即弃无从防患")


if __name__ == "__main__":
    main()
