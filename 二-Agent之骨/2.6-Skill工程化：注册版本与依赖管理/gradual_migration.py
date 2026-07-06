# 文件名: gradual_migration.py
# 功能: MAJOR 升级的灰度迁移——共存/迁移/下线三阶段
# 运行: python gradual_migration.py

"""灰度迁移：当 MAJOR 升级必须发生。

共存期: 新旧版同时注册，注册表用 skill@v1 / skill@v2 作 key
迁移期: 调用方逐步迁，监控 v1 调用量降趋势
下线期: v1 调用量=0 后删，删前发最后警告，删后返回 skill_deprecated
实测: 灰度迁移 6 周 vs 一刀切换返工 6 周，灰度反而更快。
教学版，模拟三阶段。
"""
from dataclasses import dataclass, field
import random

random.seed(42)

@dataclass
class MigrationTracker:
    callers: list[str] = field(default_factory=list)
    migrated: list[str] = field(default_factory=list)
    v1_calls: dict = field(default_factory=dict)
    deprecated_warning_sent: bool = False

    def simulate_week(self, week: int) -> dict:
        total_calls = 0
        v1_calls = 0
        for caller in self.callers:
            if caller not in self.migrated:
                if random.random() < 0.3:  # 每周 30% 概率迁移
                    self.migrated.append(caller)
            calls = random.randint(5, 20)
            total_calls += calls
            if caller not in self.migrated:
                v1_calls += calls
        self.v1_calls[week] = v1_calls
        return {"week": week, "total": total_calls, "v1": v1_calls,
                "migrated": len(self.migrated), "total_callers": len(self.callers)}

def main():
    print("=" * 64)
    print("灰度迁移：共存 → 迁移 → 下线")
    print("=" * 64)
    tracker = MigrationTracker()
    tracker.callers = [f"agent_{i}" for i in range(10)]
    print(f"\n共存期开始: {len(tracker.callers)} 个调用方, v1+v2 同时可用")
    print(f"\n{'周':<4}{'总调用':<8}{'v1 调用':<10}{'已迁移':<10}{'v1 调用率':<10}{'阶段'}")
    print("-" * 64)
    for w in range(1, 7):
        r = tracker.simulate_week(w)
        v1_rate = r["v1"] / max(r["total"], 1)
        stage = "迁移期" if v1_rate > 0.05 else "可下线"
        print(f"{w:<4}{r['total']:<8}{r['v1']:<10}"
              f"{r['migrated']}/{r['total_callers']:<8}"
              f"{v1_rate:<10.0%}{stage}")
    print()
    print("结论: v1 调用率 < 5% 即可下线")
    print("      下线前发最后警告（7 天缓冲）")
    print("      下线后 v1 调用返回 skill_deprecated（可读反馈）")
    print("      灰度迁移 6 周 vs 一刀切换返工 6 周，灰度反而更快")

if __name__ == "__main__":
    main()
