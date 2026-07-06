# 文件名: minimal_harness.py
# 功能: 六大子系统的最小可用 harness 骨架（200 行）
# 运行: python minimal_harness.py

"""Minimal Harness：模型之外的一切。

六大子系统：上下文组装、工具调度、错误恢复、
状态持久化、验证护栏、成本管控。教学版，模拟 LLM。
"""
import json
import hashlib
from dataclasses import dataclass, field
from typing import Callable

# ---------- 模拟 LLM ----------
def mock_llm(messages: list[dict]) -> str:
    last = messages[-1]["content"][:80] if messages else ""
    if "read" in last.lower():
        return '{"tool":"read_file","args":{"path":"/tmp/data.txt"}}'
    if "done" in last.lower() or "complete" in last.lower():
        return '{"tool":"finish","args":{"result":"任务完成"}}'
    return '{"tool":"read_file","args":{"path":"/tmp/step.txt"}}'

# ---------- 1. 上下文组装 ----------
@dataclass
class ContextManager:
    window: int = 8000
    recent_keep: int = 2000
    messages: list[dict] = field(default_factory=list)

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._compact()

    def _compact(self):
        total = sum(len(m["content"]) for m in self.messages)
        if total <= self.window:
            return
        sys_msgs = [m for m in self.messages if m["role"] == "system"]
        nonsys = [m for m in self.messages if m["role"] != "system"]
        kept = []
        size = 0
        for m in reversed(nonsys):
            size += len(m["content"])
            kept.insert(0, m)
            if size >= self.recent_keep:
                break
        summary = f"[前 {len(nonsys)-len(kept)} 条消息已摘要：任务进行中]"
        self.messages = sys_msgs + [{"role":"system","content":summary}] + kept

    def render(self) -> list[dict]:
        return self.messages.copy()

# ---------- 2. 工具调度 ----------
TOOL_REGISTRY: dict[str, Callable] = {}

def register_tool(name: str):
    def deco(fn: Callable):
        TOOL_REGISTRY[name] = fn
        return fn
    return deco

@register_tool("read_file")
def read_file(path: str) -> str:
    if path == "/tmp/data.txt":
        return "文件内容：销售数据 2024 Q3，总额 1.2M"
    return f"file_not_found: {path}"

@register_tool("finish")
def finish(result: str) -> str:
    return f"FINISH: {result}"

# ---------- 3. 错误恢复 ----------
@dataclass
class ErrorRecovery:
    max_consecutive: int = 3
    consecutivel: int = 0
    last_error: str = ""

    def wrap(self, tool_name: str, args: dict) -> tuple[str, bool]:
        try:
            fn = TOOL_REGISTRY[tool_name]
            result = fn(**args)
            self.consecutivel = 0
            return result, True
        except Exception as e:
            self.consecutivel += 1
            self.last_error = f"{type(e).__name__}: {e}"
            return f"error: {self.last_error}", False

    def should_abort(self) -> bool:
        return self.consecutivel >= self.max_consecutive

# ---------- 4. 验证护栏 ----------
def validate_tool_call(raw: str) -> tuple[str, dict] | None:
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if "tool" not in obj or "args" not in obj:
        return None
    if obj["tool"] not in TOOL_REGISTRY:
        return None
    return obj["tool"], obj["args"]

# ---------- 5. 状态持久化 ----------
@dataclass
class StateStore:
    checkpoint_path: str = "/tmp/agent_state.json"
    steps: list[dict] = field(default_factory=list)

    def checkpoint(self, step: dict) -> str:
        self.steps.append(step)
        return hashlib.md5(json.dumps(step).encode()).hexdigest()[:8]

    def restore(self) -> list[dict]:
        return self.steps.copy()

# ---------- 6. 成本管控 ----------
@dataclass
class CostGuard:
    budget_tokens: int = 100_000
    used: int = 0

    def consume(self, tokens: int) -> bool:
        self.used += tokens
        return self.used < self.budget_tokens

    def utilization(self) -> float:
        return self.used / self.budget_tokens

# ---------- Harness 主循环 ----------
class Harness:
    def __init__(self, task: str):
        self.ctx = ContextManager()
        self.ctx.add("system", f"任务：{task}。完成后调用 finish。")
        self.error = ErrorRecovery()
        self.state = StateStore()
        self.cost = CostGuard()
        self.loop_count = 0
        self.max_loops = 50

    def run(self) -> str:
        for i in range(self.max_loops):
            self.loop_count = i
            msgs = self.ctx.render()
            tok = sum(len(m["content"]) // 4 for m in msgs)
            if not self.cost.consume(tok):
                return f"成本熔断：已用 {self.cost.used} tokens"
            raw = mock_llm(msgs)
            parsed = validate_tool_call(raw)
            if parsed is None:
                self.ctx.add("assistant", raw)
                self.ctx.add("system", "错误：工具调用格式无效，请重试。")
                continue
            tool_name, args = parsed
            result, ok = self.error.wrap(tool_name, args)
            self.ctx.add("assistant", raw)
            self.ctx.add("tool", result)
            self.state.checkpoint({"loop": i, "tool": tool_name,
                                   "ok": ok, "result": result[:100]})
            if result.startswith("FINISH"):
                return result
            if self.error.should_abort():
                return f"连续错误熔断：{self.error.last_error}"
        return "步数耗尽"

def main():
    print("=" * 60)
    print("Minimal Harness 运行 demo")
    print("=" * 60)
    h = Harness("读取 /tmp/data.txt 并汇报内容")
    result = h.run()
    print(f"最终结果: {result}")
    print(f"循环次数: {h.loop_count}")
    print(f"token 消耗: {h.cost.used} / {h.cost.budget_tokens}")
    print(f"利用率: {h.cost.utilization():.1%}")
    print(f"checkpoint 数: {len(h.state.steps)}")
    print("\n步骤明细:")
    for s in h.state.steps:
        print(f"  loop {s['loop']}: {s['tool']} ok={s['ok']} -> {s['result'][:40]}")

if __name__ == "__main__":
    main()
