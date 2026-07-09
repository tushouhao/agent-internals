# 文件名: autonomy_levels.py
# 功能: 编码 Agent 三级自主性的形式化定义与崩溃模式映射
# 运行: python autonomy_levels.py

"""三级自主性形式化: 补全/修改/PR 的上下文范围、输出形态、落地机制差异。

承接 3.1 第 1 章: 三级不是严格的高比低好, 补全级在样板代码场景
效率比 PR 级高 10 倍(300ms vs 3min)。自主性越高延迟越高。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class AutonomyLevel:
    """单级自主性定义。"""
    name: str
    autonomy: float
    ctx_scope: str        # 上下文范围
    output_form: str      # 输出形态
    landing: str          # 落地机制
    crash_mode: str       # 崪溃模式
    latency_ms: int       # 单任务延迟
    cost_tokens: int


def main():
    print("=" * 60)
    print("编码 Agent 三级自主性形式化")
    print("=" * 60)
    levels = [
        AutonomyLevel("补全级", 0.0, "当前文件光标前",
                      "续写 1-30 行", "插入缓冲区",
                      "续写语法对但语义错", 300, 800),
        AutonomyLevel("修改级", 0.5, "整仓库 + 任务描述",
                      "多文件 diff", "写盘 + 跑测试",
                      "跨文件不一致", 45_000, 12_000),
        AutonomyLevel("PR 级", 1.0, "Issue + 仓库 + 评审历史",
                      "多提交 + 修订 + 评论", "git push + 评审循环",
                      "多提交逻辑漂移 + 评审误读", 360_000, 85_000),
    ]
    print(f"{'级':8s} {'自主性':8s} {'上下文':18s} {'输出':14s} {'落地':18s} {'崩溃':22s} {'延迟':9s}")
    for lv in levels:
        print(f"{lv.name:8s} {lv.autonomy:8.1f} {lv.ctx_scope:18s} "
              f"{lv.output_form:14s} {lv.landing:18s} {lv.crash_mode:22s} {lv.latency_ms:7d}ms")
    print("\n核心洞察:")
    print("1. 三级差异不在模型大小, 在三轴: 上下文范围/输出形态/落地机制")
    print("2. 每外扩一级, 自主决策内容多一个量级, 崩溃模式多一类")
    print("3. 自主性越高延迟越高: 0.3s -> 45s -> 360s (补全->修改->PR)")
    print("4. 补全级在样板代码场景效率比 PR 级高 10 倍 (非高比低好)")


if __name__ == "__main__":
    main()
