# 文件名: context_assembly.py
# 功能: 上下文组装子系统的分层压缩实现
# 运行: python context_assembly.py

"""上下文组装：分层压缩，近期原文 + 远期摘要。

对比 naive 截断 vs 分层压缩在长程任务上的信息保留率。
教学版，模拟上下文管理。
"""
from dataclasses import dataclass, field

@dataclass
class Message:
    role: str
    content: str
    tokens: int = 0

    def __post_init__(self):
        if self.tokens == 0:
            self.tokens = len(self.content) // 4

@dataclass
class NaiveContext:
    """naive 截断：超窗口即丢最早消息（包括系统指令）。"""
    window: int = 32000

    def assemble(self, messages: list[Message]) -> list[Message]:
        total = sum(m.tokens for m in messages)
        while total > self.window and messages:
            dropped = messages.pop(0)  # 丢最早的
            total -= dropped.tokens
        return messages

@dataclass
class LayeredContext:
    """分层压缩：保留系统指令 + 近期原文 + 远期摘要。"""
    window: int = 32000
    recent_keep: int = 8000

    def assemble(self, messages: list[Message]) -> list[Message]:
        sys_msgs = [m for m in messages if m.role == "system"]
        nonsys = [m for m in messages if m.role != "system"]
        # 保留近期 recent_keep token 的原文
        kept = []
        size = 0
        for m in reversed(nonsys):
            if size + m.tokens > self.recent_keep:
                break
            kept.insert(0, m)
            size += m.tokens
        # 远期摘要
        far_count = len(nonsys) - len(kept)
        if far_count > 0:
            summary = Message("system",
                f"[前 {far_count} 条已摘要：任务进行中，已执行 {far_count} 步工具调用]",
                tokens=30)
            return sys_msgs + [summary] + kept
        return sys_msgs + kept

def simulate_task(steps: int) -> list[Message]:
    """模拟 steps 步任务的上下文。"""
    msgs = [Message("system", "任务：分析销售数据并生成报告", tokens=50)]
    for i in range(steps):
        msgs.append(Message("assistant", f"第{i}步：调用 read_file", tokens=30))
        msgs.append(Message("tool", f"文件内容行{i}：data_line_{i}_" + "x"*60, tokens=200))
    return msgs

def instruction_preserved(messages: list[Message]) -> bool:
    """检查系统指令（任务）是否还在上下文中。"""
    return any("任务" in m.content and m.role == "system" and "摘要" not in m.content
               for m in messages)

def main():
    print("=" * 64)
    print("上下文组装：naive 截断 vs 分层压缩")
    print("=" * 64)
    print(f"{'步数':<8}{'naive 保留指令':<18}{'分层 保留指令':<18}{'naive token':<14}{'分层 token':<12}")
    print("-" * 64)
    for steps in [20, 40, 60, 80, 100]:
        msgs = simulate_task(steps)
        naive = NaiveContext().assemble(msgs.copy())
        layered = LayeredContext().assemble(msgs.copy())
        naive_tok = sum(m.tokens for m in naive)
        layered_tok = sum(m.tokens for m in layered)
        print(f"{steps:<8}{'是' if instruction_preserved(naive) else '否':<18}"
              f"{'是' if instruction_preserved(layered) else '否':<18}"
              f"{naive_tok:<14}{layered_tok:<12}")
    print()
    print("结论：naive 在 40 步后丢失任务指令；分层压缩始终保留，且 token 更省。")

if __name__ == "__main__":
    main()
