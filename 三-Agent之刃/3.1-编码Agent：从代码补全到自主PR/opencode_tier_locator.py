# 文件名: opencode_tier_locator.py
# 功能: opencode 在三级自主性中的位置定位
# 运行: python opencode_tier_locator.py

"""opencode 切片定位: 修改级为主 + PR 级提交规划为辅。

承接 3.1 第 7 章: opencode 的主 loop 是修改级(full),
辅以 PR 级的提交边界规划(partial), 评审循环需人介入。
设计权衡: 工程预算压在修改级甜点, 与第 6 章 ROI 分析一致。
3.13-3.14 会深拆其会话 loop / 多 Agent / skill 切片。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class CapabilityCell:
    """能力格: 三级 × 能力维度。"""
    tier: str
    capability: str
    status: str  # full / partial / none
    detail: str


def main():
    print("=" * 60)
    print("opencode 在三级自主性中的位置")
    print("=" * 60)
    cells = [
        CapabilityCell("补全级", "光标续写", "none", "opencode 非补全工具"),
        CapabilityCell("补全级", "五源上下文", "none", "不做补全上下文工程"),
        CapabilityCell("修改级", "多文件改", "full", "主 loop 跨文件 diff"),
        CapabilityCell("修改级", "测试闭环", "full", "跑测试 + traceback 清洗"),
        CapabilityCell("修改级", "影响面分析", "partial", "符号引用图 + 测试图"),
        CapabilityCell("修改级", "跨仓库扫", "none", "仅当前仓库"),
        CapabilityCell("PR 级", "提交边界规划", "partial", "拆提交但语义浅"),
        CapabilityCell("PR 级", "评审反馈分类", "none", "需人介入"),
        CapabilityCell("PR 级", "修订循环", "none", "不自主修订"),
    ]
    for c in cells:
        print(f"  [{c.tier:5s}] {c.capability:12s} {c.status:8s} {c.detail}")
    print("\n定位: opencode = 修改级 full + PR 级 partial")
    print("设计权衡: 工程预算压在修改级甜点, 评审循环留人")
    print("承接 3.13: 会话 loop 状态机切片 -> 修改级主 loop 怎么跑")
    print("承接 3.14: skill 注入 + 多 Agent 切片 -> 提交规划怎么做")


if __name__ == "__main__":
    main()
