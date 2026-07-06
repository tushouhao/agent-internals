# 文件名: lifecycle.py
# 功能: Skill 生命周期——开发/灰度/稳定/弃用四阶段
# 运行: python lifecycle.py

"""Skill 生命周期：开发→灰度→稳定→弃用。

开发期 v0.x: 接口不稳，限测试 agent 调用
灰度期 v1.0-rc: 小范围试，灰度名单内可调
稳定期 v1.x: 全范围用，监控调用量与错误率
弃用期 v1（v2 出后）: 注入弃用警告，限期迁移
每阶段 harness 区别对待，人工决策推进。
教学版，模拟生命周期。
"""
from dataclasses import dataclass

@dataclass
class SkillLifecycle:
    stage: str           # dev / rc / stable / deprecated
    version: str
    allowed_callers: list   # dev/rc 限调用方
    deprecated_until: str = ""

    def can_call(self, caller: str) -> tuple:
        if self.stage == "dev":
            return False, "开发期，仅测试 agent 可调"
        if self.stage == "rc" and caller not in self.allowed_callers:
            return False, "灰度期，仅灰度名单内可调"
        if self.stage == "deprecated":
            return True, f"弃用警告: migrate to v2 by {self.deprecated_until}"
        return True, ""

def main():
    print("=" * 64)
    print("Skill 生命周期：开发/灰度/稳定/弃用")
    print("=" * 64)
    cases = [
        ("dev", "v0.3.0", ["test_agent"], ""),
        ("rc", "v1.0-rc", ["early_adopter_1", "early_adopter_2"], ""),
        ("stable", "v1.2.0", [], ""),
        ("deprecated", "v1.2.0", [], "2026-08-01"),
    ]
    print(f"\n{'阶段':<12}{'版本':<12}{'调用方':<16}{'允许':<8}{'反馈'}")
    print("-" * 64)
    for stage, ver, allowed, dep_until in cases:
        lc = SkillLifecycle(stage, ver, allowed, dep_until)
        caller = "prod_agent"
        ok, msg = lc.can_call(caller)
        print(f"{stage:<12}{ver:<12}{caller:<16}"
              f"{'是' if ok else '否':<8}{msg[:30]}")
    print()
    print("结论: dev/rc 限调用方，stable 全可用，deprecated 注入警告")
    print("      阶段切换是人工决策，团队每周 review")

if __name__ == "__main__":
    main()
