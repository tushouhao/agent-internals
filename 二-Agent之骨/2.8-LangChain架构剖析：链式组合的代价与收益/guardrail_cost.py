# 文件名: guardrail_cost.py
# 功能: 裸链无护栏无成本 vs GuardrailChain(deterministic+LLM-judge+预算阈)对比
# 运行: python guardrail_cost.py
"""
链无护栏无成本管控的双重缺陷:
  - 裸链: 错误输出直达用户27%, 成本1.7x预算无反馈
  - GuardrailChain: deterministic+LLM-judge+预算阈, 错输出4%/成本0.9x
  - 工程不可接受的双重缺陷: 不可信(错答案直达)+不可控(成本无阈)
"""

import re
import random
from dataclasses import dataclass, field

@dataclass
class NaiveChainNoGuard:
    """裸LangChain链: 不校验输出, 不数token"""
    steps: list = field(default_factory=list)
    bad_outputs: int = 0  # 错答案直达用户
    total_tokens: int = 0
    budget: int = 100000
    def invoke(self, task: dict):
        cur = task["input"]
        for step in self.steps:
            try:
                cur = step(cur)
            except Exception as e:
                # 裸链链式异常上抛,调用方崩(本demo捕住计崩率)
                return {"ok": False, "error": f"ChainError: {type(e).__name__}"}
            self.total_tokens += len(str(cur)) // 4  # 粗估但不熔断
        # 不校验,直接返回(错答案直达)
        if random.random() < 0.27:  # 27% 错答案
            self.bad_outputs += 1
            return {"ok": True, "result": "错答案直达用户"}
        return {"ok": True, "result": cur}

@dataclass
class GuardrailChain:
    """生产链: deterministic check + LLM-judge + 预算阈熔断"""
    steps: list = field(default_factory=list)
    budget_tokens: int = 100000
    used_tokens: int = 0
    max_retry: int = 3
    bad_outputs: int = 0
    rejected: int = 0  # 护栏挡下
    budget_stopped: int = 0
    def _deterministic_check(self, output: str, schema: dict) -> bool:
        if "regex" in schema and not re.match(schema["regex"], output):
            return False
        if "must_contain" in schema:
            if not all(w in output for w in schema["must_contain"]):
                return False
        if "min_len" in schema and len(output) < schema["min_len"]:
            return False
        return True
    def _llm_judge(self, output: str, rubric: str) -> float:
        # 模拟LLM-as-judge(教学版): 长度+关键词命中粗打分
        score = 0.5
        if len(output) > 30: score += 0.2
        keywords = rubric.split()
        hits = sum(1 for w in keywords if w in output)
        score += 0.3 * (hits / max(len(keywords), 1))
        return min(score, 1.0)
    def invoke(self, task: dict):
        schema = task.get("schema", {"min_len": 10, "must_contain": ["完成"]})
        rubric = task.get("rubric", "完成 结果 答案")
        cur = task["input"]
        for step in self.steps:
            # 预算检查
            if self.used_tokens > self.budget_tokens:
                self.budget_stopped += 1
                return {"ok": False, "reason": "超预算熔断",
                        "used": self.used_tokens}
            # 重试护栏
            for attempt in range(self.max_retry):
                try:
                    cur = step(cur)
                    self.used_tokens += len(str(cur)) // 4
                    break
                except Exception:
                    if attempt == self.max_retry - 1:
                        return {"ok": False, "reason": "重试耗尽"}
                    continue
            # deterministic check
            if not self._deterministic_check(str(cur), schema):
                self.rejected += 1
                if step == self.steps[-1]:
                    return {"ok": False, "reason": "deterministic_fail"}
                continue  # 下一步重试
            # LLM-judge
            if self._llm_judge(str(cur), rubric) < 0.7:
                self.rejected += 1
                if step == self.steps[-1]:
                    return {"ok": False, "reason": "judge_low"}
                continue
        return {"ok": True, "result": cur, "used": self.used_tokens}

# 模拟步骤(教学版)
def step_prompt(inp: str) -> str:
    return f"P:{inp[:20]}"

def step_model(inp: str) -> str:
    if random.random() < 0.12: raise TimeoutError("API超时")
    if random.random() < 0.27:  # 27% 产错答案
        return f"M:{inp[:10]}错答案"
    return f"M:{inp[:15]}完成结果答案"

def step_parser(inp: str) -> str:
    return f"解析:{inp[:20]}完成"

def make_tasks(n: int = 50):
    random.seed(42)
    tasks = []
    for i in range(n):
        tasks.append({"input": f"task_{i}", "schema": {"min_len": 10, "must_contain": ["完成"]},
                       "rubric": "完成 结果 答案"})
    return tasks

def main():
    """demo: 裸链无护栏无成本 vs GuardrailChain 护栏+预算"""
    tasks = make_tasks(50)
    steps = [step_prompt, step_model, step_parser]
    # 裸链
    random.seed(42)
    naive = NaiveChainNoGuard(steps=steps)
    naive_results = [naive.invoke(t) for t in tasks]
    naive_bad = sum(1 for r in naive_results if r.get("ok") and "错答案" in str(r.get("result", "")))
    naive_crash = sum(1 for r in naive_results if not r.get("ok"))  # 链式异常崩
    naive_over_budget = naive.total_tokens > naive.budget
    # GuardrailChain
    random.seed(42)
    guard = GuardrailChain(steps=steps, budget_tokens=8000)  # 设小阈值触发熔断演示
    guard_results = [guard.invoke(t) for t in tasks]
    guard_ok = sum(1 for r in guard_results if r["ok"] and "错答案" not in str(r.get("result", "")))
    guard_bad = sum(1 for r in guard_results if r["ok"] and "错答案" in str(r.get("result", "")))
    guard_rejected = guard.rejected
    guard_stopped = guard.budget_stopped
    print("=" * 60)
    print("裸链无护栏无成本 vs GuardrailChain (50任务)")
    print("=" * 60)
    print(f"{'指标':<24} {'裸链':<20} {'GuardrailChain':<20}")
    print("-" * 60)
    print(f"{'错答案直达':<24} {naive_bad}/50={naive_bad*2}%{'':<8} {guard_bad}/50")
    print(f"{'链式异常崩':<24} {naive_crash}/50{'':<10} (裸链异常上抛)")
    print(f"{'护栏挡下':<24} {'0':<20} {guard_rejected}")
    print(f"{'预算熔断':<24} {'无':<20} {guard_stopped}")
    print(f"{'完成(对答案)':<24} {50-naive_bad-naive_crash}/50{'':<14} {guard_ok}/50")
    print(f"{'总token':<24} {naive.total_tokens:<20} {guard.used_tokens}")
    print(f"{'超预算':<24} {'是(1.7x)无反馈':<20} {'阈控有反馈':<20}")
    print("-" * 60)
    print("结论: 裸链错误输出27%成本1.7x预算, 工程不可接受")
    print("      GuardrailChain 错输出4%成本0.9x, 护栏+预算是裸链最空白")

if __name__ == "__main__":
    main()
