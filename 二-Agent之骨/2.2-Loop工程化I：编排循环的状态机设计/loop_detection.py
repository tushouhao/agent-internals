# 文件名: loop_detection.py
# 功能: 死循环检测——轨迹指纹与降级处置
# 运行: python loop_detection.py

"""死循环检测：连续相同调用与轨迹指纹。

粗粒度：连续 3 步 (tool,args) 元组全相同
细粒度：连续 5 步 tool 相同 + 完成度无提升
降级：强制换工具；escalate：连续 2 次降级仍循环
教学版，模拟 Agent 轨迹。
"""
import hashlib
from dataclasses import dataclass, field

@dataclass
class LoopDetector:
    """轨迹指纹死循环检测。"""
    window: int = 3                # 检测窗
    hashes: list[str] = field(default_factory=list)
    degrade_count: int = 0        # 降级次数
    max_degrade: int = 2          # 连续 2 次降级即 escalate

    def fingerprint(self, tool: str, args: dict) -> str:
        """对 (tool, args) 取 hash 作为指纹。"""
        raw = f"{tool}|{sorted(args.items())}"
        return hashlib.md5(raw.encode()).hexdigest()[:8]

    def observe(self, tool: str, args: dict) -> str:
        """观察一步动作，返回 'normal' / 'degrade' / 'escalate'。"""
        fp = self.fingerprint(tool, args)
        self.hashes.append(fp)
        if len(self.hashes) > self.window:
            self.hashes.pop(0)
        # 连续 window 步指纹全相同
        if len(self.hashes) >= self.window and len(set(self.hashes)) == 1:
            self.degrade_count += 1
            if self.degrade_count >= self.max_degrade:
                return "escalate"
            return "degrade"
        return "normal"

    def reset_after_degrade(self):
        """降级处置后重置指纹窗。"""
        self.hashes.clear()

def simulate_trajectory(steps: int, loop_at: int = 15) -> list[tuple[str, dict]]:
    """模拟 steps 步轨迹，在 loop_at 步开始死循环。"""
    traj = []
    for i in range(steps):
        if i < loop_at:
            traj.append(("read_file", {"path": f"/tmp/f{i}.txt"}))
        else:
            # 死循环：反复读同一文件
            traj.append(("read_file", {"path": "/tmp/loop.txt"}))
    return traj

def main():
    print("=" * 64)
    print("死循环检测：轨迹指纹与降级处置")
    print("=" * 64)
    detector = LoopDetector(window=3)
    traj = simulate_trajectory(25, loop_at=15)
    print("\n轨迹观察（25 步，第 15 步起死循环）：")
    print(f"{'步':<6}{'工具':<14}{'指纹':<12}{'处置':<12}")
    print("-" * 64)
    stats = {"normal": 0, "degrade": 0, "escalate": 0}
    escalated = False
    for i, (tool, args) in enumerate(traj):
        if escalated:
            break
        fp = detector.fingerprint(tool, args)
        action = detector.observe(tool, args)
        stats[action] += 1
        print(f"{i+1:<6}{tool:<14}{fp:<12}{action:<12}")
        if action == "degrade":
            detector.reset_after_degrade()
            print(f"{'':6}{'→ 降级处置：强制换工具 1 步'}")
        elif action == "escalate":
            escalated = True
            print(f"{'':6}{'→ escalate：人工接管'}")
    print(f"\n统计: normal={stats['normal']}, degrade={stats['degrade']}, escalate={stats['escalate']}")
    print("结论：粗粒度检测在连续 3 步同调用时触发，2 次降级后 escalate。")

if __name__ == "__main__":
    main()
