# 文件名: version_management.py
# 功能: SemVer 语义版本号与 breaking change 界定
# 运行: python version_management.py

"""Skill 版本管理：SemVer 与 breaking change。

SemVer: MAJOR.MINOR.PATCH
MAJOR: 不兼容升级（删字段/改类型），调用方必须改
MINOR: 兼容新增（加字段/加功能），调用方不用改
PATCH: 修复（bug fix），调用方不用改
breaking 界定标准: 调用方代码是否需要改
不确定时按 breaking 处理（升 MAJOR），误判为兼容是最大坑。
教学版，模拟版本升级。
"""
from dataclasses import dataclass

@dataclass
class VersionInfo:
    major: int
    minor: int
    patch: int
    def __str__(self): return f"v{self.major}.{self.minor}.{self.patch}"
    def bump(self, level: str) -> "VersionInfo":
        if level == "MAJOR":
            return VersionInfo(self.major + 1, 0, 0)
        if level == "MINOR":
            return VersionInfo(self.major, self.minor + 1, 0)
        return VersionInfo(self.major, self.minor, self.patch + 1)

def classify_change(removed_params: bool, changed_types: bool,
                    added_params: bool, added_returns: bool, bug_fix: bool) -> str:
    if removed_params or changed_types:
        return "MAJOR"
    if added_params or added_returns:
        return "MINOR"
    return "PATCH"

def main():
    print("=" * 64)
    print("SemVer 语义版本号与 breaking change 界定")
    print("=" * 64)
    v = VersionInfo(1, 2, 0)
    print(f"\n当前版本: {v}")
    changes = [
        ("删了 agg 参数", True, False, False, False, False),
        ("改了 path 类型 str→Path", False, True, False, False, False),
        ("加了 output_format 参数", False, False, True, False, False),
        ("加了返回字段 warnings", False, False, False, True, False),
        ("修复空 CSV 崩溃", False, False, False, False, True),
    ]
    print(f"\n{'变更':<26}{'类型':<8}{'新版本':<12}{'调用方'}")
    print("-" * 64)
    for desc, rm, ct, ap, ar, bf in changes:
        level = classify_change(rm, ct, ap, ar, bf)
        new_v = v.bump(level)
        caller = "必须改" if level == "MAJOR" else "不用改"
        print(f"{desc:<26}{level:<8}{str(new_v):<12}{caller}")
    print()
    print("结论: 不确定时按 breaking 处理（升 MAJOR）")
    print("      误判 breaking 为兼容是版本管理最大坑")

if __name__ == "__main__":
    main()
