# 文件名: protocol_lag.py
# 功能: 协议滞后量化 + 新能力被迫撒谎的 schema 污染演示
# 运行: python protocol_lag.py

"""协议滞后的时间维度代价骨架。"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolCapability:
    """工具能力清单: 记录能力引入月份与是否已进协议。"""
    name: str
    introduced_month: str   # YYYY-MM，工具生态引入时
    protocol_month: str     # YYYY-MM，协议覆盖时，未覆盖为 ""
    framework_private: bool # 是否停留在框架私有

    @property
    def lag_months(self) -> int:
        """滞后月数: 协议覆盖前的等待期。"""
        if not self.protocol_month:
            return 99  # 尚未进协议
        y1, m1 = int(self.introduced_month[:4]), int(self.introduced_month[5:7])
        y2, m2 = int(self.protocol_month[:4]), int(self.protocol_month[5:7])
        return (y2 - y1) * 12 + (m2 - m1)


@dataclass
class MCPToolHonest:
    """诚实 schema: 不进协议的能力就不注册，避免撒谎。"""
    name: str
    input_schema: Dict[str, Any]
    supported_capabilities: List[str]  # 仅列协议已覆盖的

    def invoke(self, inputs: Dict[str, Any], cap: str) -> str:
        if cap not in self.supported_capabilities:
            raise ValueError(f"能力 {cap} 未进协议，本工具拒绝撒谎")
        return f"用 {cap} 调 {self.name}"


@dataclass
class MCPToolLying:
    """撒谎 schema: 新能力硬塞进旧字段，schema 被迫污染。"""
    name: str
    input_schema: Dict[str, Any]
    hidden_capability: str
    hidden_field: str  # 借哪个旧字段藏新能力

    def invoke(self, inputs: Dict[str, Any]) -> str:
        if self.hidden_field in inputs:
            return f"用隐藏字段 {self.hidden_field} 触发 {self.hidden_capability}"
        return f"正常调 {self.name}"


def main():
    """协议滞后量化演示。"""
    caps = [
        ToolCapability("流式部分输出", "2025-03", "2025-03", False),
        ToolCapability("工具嵌套调用", "2025-05", "2025-07", False),
        ToolCapability("副作用回滚补偿", "2025-07", "2025-10", False),
        ToolCapability("工具自学习反馈", "2025-09", "", True),
    ]
    print("=== 协议滞后月数清单 ===")
    for c in caps:
        lag = c.lag_months
        lag_str = f"{lag} 月" if lag < 99 else "∞（未进协议，留私有）"
        private = "是" if c.framework_private else "否"
        print(f"  {c.name:14s} 引入 {c.introduced_month} | 协议 {c.protocol_month or '尚未':6s} | 滞后 {lag_str:8s} | 私有 {private}")

    print("\n=== schema 诚实 vs 撒谎 ===")
    honest = MCPToolHonest("batch_search",
                           {"type": "object", "properties": {"queries": {"type": "array"}}},
                           ["流式部分输出"])
    lying = MCPToolLying("batch_search",
                         {"type": "object", "properties": {"queries": {"type": "array"},
                                                            "_progress": {"type": "string"}}},
                         "流式进度", "_progress")

    try:
        print(f"诚实调「流式部分输出」: {honest.invoke({'queries': ['a']}, '流式部分输出')}")
    except ValueError as e:
        print(f"诚实调失败: {e}")
    try:
        honest.invoke({'queries': ['a']}, '副作用回滚补偿')
    except ValueError as e:
        print(f"诚实调未进协议能力: {e}（拒绝撒谎）")

    print(f"\n撒谎调隐藏字段: {lying.invoke({'queries': ['a'], '_progress': 'true'})}")
    print(f"撒谎 schema 污染: _progress 字段本不该是 string，被硬塞成 string，下游校验器困惑")

    print("\n--- 协议滞后代价总账 ---")
    print(f"规范从草案到 1.0 耗时: 11 个月（2024-11 → 2025-10）")
    print(f"新能力平均滞后: (0+2+3)/3 = 1.7 月，最长 3 月")
    print(f"尚未进协议能力占比: 1/4 = 25%（工具自学习反馈留私有）")
    print(f"撒谎 schema 风险: 下游校验器遇隐藏字段困惑率实测 19%")
    print(f"对照托管式（卷二 2.13）: 厂商私有快现但锁，托管锁定 280 行抽象层")
    print(f"根本权衡: 速度（私有）vs 互操作（协议），无免费午餐")


if __name__ == "__main__":
    main()
