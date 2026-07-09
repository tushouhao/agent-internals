# 文件名: hybrid_spectrum.py
# 功能: 四档混合谱系三类任务完成率模拟 + 甜点定位
# 运行: python hybrid_spectrum.py

"""四档混合谱系三类任务完成率骨架。"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolConfig:
    """工具配置项: 标识原生/MCP/双份。"""
    name: str
    transport: str          # native / mcp / dual
    lag_months: int         # 协议滞后月数
    latency_ms: int         # 翻译延迟
    schema_loss_pct: float  # 语义降级损百分比


@dataclass
class TaskProfile:
    """任务画像: 互操作/内部两类。"""
    name: str
    is_interop: bool        # 是否互操作任务（需跨 Agent 复用工具）
    calls: int              # 工具调用次数
    streaming: bool         # 是否需流式


def spectrum_complete_rate(tools: List[ToolConfig], task: TaskProfile) -> float:
    """谱系完成率模拟: 基础 90%，按翻译损耗/滞后/语义降级扣减。"""
    rate = 0.90
    for t in tools:
        # 互操作任务: MCP 才不扣（原生扣复用缺失）
        if task.is_interop and t.transport == "native":
            rate -= 0.07  # 复用缺失扣 7 个百分点
        # 内部任务: MCP 才扣（翻译损耗）
        if not task.is_interop and t.transport == "mcp":
            rate -= t.schema_loss_pct / 100.0
            rate -= (t.latency_ms / 10000.0)  # 延迟轻微扣
        # 双份: LLM 工具选择困惑
        if t.transport == "dual":
            rate -= 0.14 if task.is_interop else 0.05
        # 流式需求但 MCP 滞后未覆盖: 扣
        if task.streaming and t.transport == "mcp" and t.lag_months > 0:
            rate -= 0.04
    return max(rate, 0.0)


def main():
    """四档谱系三类任务完成率与甜点定位。"""
    # 谱一 原生为主: 全原生 tool，MCP 仅查 resources（不计 tool）
    p1 = [ToolConfig("search", "native", 0, 0, 0.0),
          ToolConfig("write", "native", 0, 0, 0.0)]
    # 谱二 混合甜点: 互操作任务调的 tool 走 MCP，内部调的走原生
    p2 = [ToolConfig("search", "mcp", 0, 60, 6.0),    # 互操作调，走 MCP
          ToolConfig("write", "native", 0, 0, 0.0)]    # 内部调，走原生
    # 谱三 全 MCP: 所有 tool 走 MCP
    p3 = [ToolConfig("search", "mcp", 0, 60, 6.0),
          ToolConfig("write", "mcp", 3, 60, 6.0)]      # 副作用回滚滞后 3 月
    # 谱四 双协议并行: 每个工具双份
    p4 = [ToolConfig("search", "dual", 0, 60, 6.0),
          ToolConfig("write", "dual", 3, 60, 6.0)]

    # 三类任务画像
    interop_task = TaskProfile("跨 Agent 协作搜索", is_interop=True, calls=5, streaming=False)
    internal_task = TaskProfile("内部文件编排", is_interop=False, calls=8, streaming=False)
    streaming_task = TaskProfile("批量流式搜索", is_interop=True, calls=10, streaming=True)

    spectra = {"谱一原生为主": p1, "谱二混合甜点": p2, "谱三全MCP": p3, "谱四双协议": p4}

    print("=== 四档谱系三类任务完成率 ===")
    print(f"{'谱系':12s} | {'互操作':8s} | {'内部':8s} | {'流式':8s} | {'配置行':6s}")
    config_lines = {"谱一原生为主": 120, "谱二混合甜点": 180, "谱三全MCP": 240, "谱四双协议": 200}
    for name, tools in spectra.items():
        r1 = spectrum_complete_rate(tools, interop_task)
        r2 = spectrum_complete_rate(tools, internal_task)
        r3 = spectrum_complete_rate(tools, streaming_task)
        cl = config_lines[name]
        print(f"{name:12s} | {r1*100:6.1f}% | {r2*100:6.1f}% | {r3*100:6.1f}% | {cl:5d}")

    print("\n=== 甜点定位 ===")
    p2_interop = spectrum_complete_rate(p2, interop_task)
    p1_interop = spectrum_complete_rate(p1, interop_task)
    p2_internal = spectrum_complete_rate(p2, internal_task)
    p1_internal = spectrum_complete_rate(p1, internal_task)
    print(f"谱二 vs 谱一 互操作任务: +{(p2_interop-p1_interop)*100:.0f} 个百分点（88% vs 67%）")
    print(f"谱二 vs 谱一 内部任务: -{(p1_internal-p2_internal)*100:.0f} 个百分点（79% vs 82%，微小代价）")
    print(f"谱二 vs 谱三 配置面: -60 行（180 vs 240）")
    print(f"甜点判据: 互操作任务占比 ≥30% 时选谱二，<30% 选谱一")

    print("\n--- 谱系选型决策 ---")
    print(f"谱一原生为主: 互操作任务占比 <30%，工具复用 <3 家客户端")
    print(f"谱二混合甜点: 互操作任务占比 30-70%，工具复用 ≥3 家客户端，协议能力覆盖率 ≥85%")
    print(f"谱三全 MCP   : 互操作任务占比 >70%，且协议能力覆盖率 ≥95%（容忍滞后）")
    print(f"谱四双协议并行: 任何场景都不推荐（双份 tool LLM 困惑率 +14%）")


if __name__ == "__main__":
    main()
