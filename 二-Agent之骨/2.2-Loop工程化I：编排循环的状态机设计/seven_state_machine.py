# 文件名: seven_state_machine.py
# 功能: 7 状态 5 边的生产级 loop 状态机骨架
# 运行: python seven_state_machine.py

"""七状态五边：生产级 Loop 最小状态机。

状态: init/plan/act/observe/retry/pause/finish/escalate/abort
转换边: 成功推进/失败重试/阈值熔断/审批暂停/完成终止
教学版，模拟 LLM 与工具调用。
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

class State(Enum):
    INIT = "init"
    PLAN = "plan"
    ACT = "act"
    OBSERVE = "observe"
    RETRY = "retry"
    PAUSE = "pause"
    FINISH = "finish"
    ESCALATE = "escalate"
    ABORT = "abort"

# 模拟 LLM 决策
def mock_llm_plan(ctx: dict) -> tuple[str, dict]:
    step = ctx.get("step", 0)
    if step >= 3:
        return "finish", {"result": "任务完成"}
    return "read_file", {"path": f"/tmp/file_{step}.txt"}

# 模拟工具
def read_file(path: str) -> str:
    if "file_0" in path or "file_1" in path:
        return "ok: 内容读取成功"
    return "error: file_not_found"

@dataclass
class StateMachine:
    max_steps: int = 5
    max_retry: int = 3
    state: State = State.INIT
    step: int = 0
    retry_count: int = 0
    ctx: dict = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)

    def transition(self) -> State:
        """状态转换主逻辑：返回下一态。"""
        self.history.append({"from": self.state.value, "step": self.step})
        if self.state == State.INIT:
            self.ctx["step"] = 0
            self.state = State.PLAN
            return self.state
        if self.state == State.PLAN:
            self.step += 1
            if self.step > self.max_steps:
                self.state = State.ESCALATE
                return self.state
            tool, args = mock_llm_plan(self.ctx)
            self.ctx["last_tool"] = tool
            self.ctx["last_args"] = args
            self.state = State.ACT
            return self.state
        if self.state == State.ACT:
            tool = self.ctx.get("last_tool", "")
            args = self.ctx.get("last_args", {})
            if tool == "finish":
                self.state = State.FINISH
                return self.state
            result = read_file(args.get("path", ""))
            self.ctx["last_result"] = result
            if "ok" in result:
                self.retry_count = 0
                self.state = State.OBSERVE
            else:
                self.retry_count += 1
                self.state = State.RETRY
            return self.state
        if self.state == State.OBSERVE:
            self.ctx["step"] = self.step
            self.state = State.PLAN
            return self.state
        if self.state == State.RETRY:
            if self.retry_count >= self.max_retry:
                self.state = State.ESCALATE
            else:
                self.state = State.ACT
            return self.state
        return self.state

    def is_terminal(self) -> bool:
        return self.state in (State.FINISH, State.ESCALATE, State.ABORT)

def main():
    print("=" * 60)
    print("七状态五边：生产级 Loop 状态机 demo")
    print("=" * 60)
    sm = StateMachine()
    print(f"初始态: {sm.state.value}")
    while not sm.is_terminal():
        sm.transition()
        print(f"  → {sm.state.value} (step={sm.step}, retry={sm.retry_count})")
    print(f"\n最终态: {sm.state.value}")
    print(f"总步数: {sm.step}, 重试: {sm.retry_count}")
    print(f"状态轨迹长度: {len(sm.history)}")
    print("\n轨迹:")
    for h in sm.history:
        print(f"  {h['from']} (step {h['step']})")

if __name__ == "__main__":
    main()
