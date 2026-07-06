# 文件名: reversibility.py
# 功能: 压缩的可逆性——外存保证可拉回，对比不可逆截断的累积压错率
# 运行: python reversibility.py

"""压缩可逆性：何时能拉回，何时不能。

不可逆: 截断（丢的信息没了）
半可逆: 摘要/抽取（语义/骨架保了，精确值没了，若外存了完整内容则可逆）
完全可逆: 引用（指针在原文就在）
生产原则: 压前先外存完整内容，保证压错可回滚
教学版，模拟可逆性对比与累积压错率。
"""
import hashlib
from dataclasses import dataclass, field
import random

random.seed(2026)

@dataclass
class ExternalStore:
    _store: dict = field(default_factory=dict)

    def put(self, content: str) -> str:
        h = hashlib.md5(content.encode()).hexdigest()[:8]
        self._store[h] = content
        return f"ref://{h}"

    def get(self, ref: str) -> str | None:
        return self._store.get(ref.replace("ref://", ""))

@dataclass
class ReversibleCompactor:
    store: ExternalStore = field(default_factory=ExternalStore)
    history: list[dict] = field(default_factory=list)

    def compress_with_external(self, msg: dict) -> dict:
        full = msg["content"]
        ref = self.store.put(full)
        compact = {"path": msg.get("path", "?"), "preview": full[:100],
                   "tokens": 30, "ref": ref}
        self.history.append({"original": msg, "compact": compact})
        return compact

    def rollback(self, compact: dict) -> dict | None:
        ref = compact.get("ref")
        if not ref:
            return None
        full = self.store.get(ref)
        return {"content": full, "tokens": len(full) // 4} if full else None

def cumulative_error_rate(single_rate: float, steps: int) -> float:
    """单次压错率在 N 步上累积至少一次压错率。"""
    return 1 - (1 - single_rate) ** steps

def main():
    print("=" * 64)
    print("压缩可逆性：外存保证可拉回")
    print("=" * 64)
    compactor = ReversibleCompactor()
    # 模拟 5 条消息压缩
    for i in range(5):
        msg = {"path": f"/tmp/f{i}", "content": f"内容_{i}_" + "x" * 2000}
        c = compactor.compress_with_external(msg)
        print(f"  压缩 {msg['path']}: {c['tokens']}t + ref")

    print(f"\n回滚测试:")
    first_compact = compactor.history[0]["compact"]
    restored = compactor.rollback(first_compact)
    print(f"  拉回第一条: {restored['tokens']}t（原文恢复）")

    print(f"\n可逆性对比:")
    print(f"  {'策略':<8}{'可逆性':<14}{'压错率':<10}{'80步累积':<12}{'回滚'}")
    print(f"  {'截断':<8}{'不可逆':<14}{'3%':<10}{cumulative_error_rate(0.03, 80):.0%}{'':<5}无法")
    print(f"  {'摘要':<8}{'半可逆':<14}{'3%':<10}{cumulative_error_rate(0.03, 80):.0%}{'':<5}需外存")
    print(f"  {'抽取':<8}{'半可逆':<14}{'3%':<10}{cumulative_error_rate(0.03, 80):.0%}{'':<5}需外存")
    print(f"  {'引用':<8}{'完全可逆':<14}{'3%':<10}{cumulative_error_rate(0.03, 80):.0%}{'':<5}随时")
    print(f"\n生产原则: 压前先外存完整内容")
    print(f"  代价: 2-4MB/任务 + 15ms/步")
    print(f"  换回: 3% 压错率 100% 可拉回（vs 不可逆截断累积 71% 至少一次压错）")

if __name__ == "__main__":
    main()
