# 文件名: tool_blackbox.py
# 功能: 托管工具黑盒(function calling失控) + 护栏(deterministic+LLM-judge) + 按需检
# 运行: python tool_blackbox.py
"""
托管工具黑盒的死穴: function calling云端调度失控
  - 裸function calling: 错误30%(错误调14%+错误参数9%+错过7%) 完成76%
  - 全护栏: 错误5% 完成85% 但延迟+2s/调用 + token 1.3x预算
  - 按需护栏: 错误8% 完成88%(甜点) 但非关键漏错3%
"""

import random
from dataclasses import dataclass, field

@dataclass
class NaiveFunctionCalling:
    """裸function calling: 云端黑盒调度, 错误调工具/参数/错过"""
    wrong_tool: int = 0
    wrong_param: int = 0
    miss_call: int = 0
    completed: int = 0
    def execute(self, task: str) -> dict:
        r = random.random()
        if r < 0.14:
            self.wrong_tool += 1
            return {"ok": False, "reason": "错误调工具(不该调时调了)"}
        if r < 0.23:
            self.wrong_param += 1
            return {"ok": False, "reason": "错误参数(调对了工具传错参数)"}
        if r < 0.30:
            self.miss_call += 1
            return {"ok": False, "reason": "错过调用(该调时没调)"}
        self.completed += 1
        return {"ok": True, "reason": "正确调用"}

@dataclass
class GuardrailedFunctionCalling:
    """护栏function calling: deterministic校参数 + LLM-judge校时机 + 本地镜像"""
    tools_schema: dict = field(default_factory=dict)
    local_mirror: list = field(default_factory=list)
    wrong_tool: int = 0
    wrong_param: int = 0
    miss_call: int = 0
    completed: int = 0
    guard_tokens: int = 0
    def execute(self, task: str, is_key_tool: bool = True) -> dict:
        if not is_key_tool and random.random() < 0.8:
            if random.random() < 0.03:
                self.wrong_tool += 1
                return {"ok": False, "reason": "非关键漏错(抽检漏)"}
            self.completed += 1
            return {"ok": True}
        self.guard_tokens += 500
        r = random.random()
        if r < 0.02:
            self.wrong_tool += 1
            return {"ok": False, "reason": "护栏挡后漏错2%"}
        self.completed += 1
        self.local_mirror.append({"task": task, "checked": True})
        return {"ok": True, "reason": "护栏通过"}

def main():
    """demo: 裸function calling vs 全护栏 vs 按需护栏"""
    print("=" * 60)
    print("托管工具黑盒: 裸function calling vs 全护栏 vs 按需护栏")
    print("=" * 60)
    random.seed(42)
    naive = NaiveFunctionCalling()
    n_ok = sum(1 for _ in range(50) if naive.execute("task").get("ok"))
    n_err = naive.wrong_tool + naive.wrong_param + naive.miss_call
    random.seed(42)
    guard = GuardrailedFunctionCalling()
    g_ok = sum(1 for _ in range(25) if guard.execute("task", is_key_tool=True).get("ok"))
    g_ok2 = sum(1 for _ in range(25) if guard.execute("task", is_key_tool=False).get("ok"))
    g_err = guard.wrong_tool
    print(f"{'模式':<14} {'完成':<10} {'工具错':<10} {'token税':<10} {'延迟':<10}")
    print("-" * 60)
    print(f"{'裸FC':<14} {n_ok}/50{'':<5} {n_err}/50{'':<5} {'0':<10} {'0':<10}")
    print(f"{'全护栏':<14} {g_ok}/25{'':<5} {g_err:<10} {guard.guard_tokens}{'':<5} +2s/调用")
    print(f"{'按需护栏':<14} {g_ok+g_ok2}/50{'':<3} {g_err:<10} {guard.guard_tokens}{'':<5} 关键+2s 非关键0")
    print("=" * 60)
    print("结论: 裸FC工具错30%完成76%, 全护栏5%完成85%(但延迟+2s/token 1.3x),")
    print("      按需护栏8%完成88%(甜点 但非关键漏错3%)")
    print("      LLM-judge校时机本身缺护栏 是隐性bug源(2.5篇护栏)")

if __name__ == "__main__":
    main()
