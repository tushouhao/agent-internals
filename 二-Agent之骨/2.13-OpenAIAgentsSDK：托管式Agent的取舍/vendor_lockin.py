# 文件名: vendor_lockin.py
# 功能: 托管锁锁定(vendor lock-in) + 抽象层(LiteLLM) + 本地镜像 + 开标协议(MCP)
# 运行: python vendor_lockin.py
"""
托管锁锁定的死穴: state/tools/loop全在云端迁移即重写
  - 裸锁定: 切换成本280行(Threads导出+function适配+loop自研)
  - LiteLLM抽象层: 切换80行 但延迟+200ms + 滞后3周
  - 原生API+本地镜像: 切换120行(甜点 保新功能+数据有底)
"""

from dataclasses import dataclass

@dataclass
class NaiveVendorLock:
    """裸托管锁: Threads/Runs/function全在云端, 迁移即重写"""
    platform: str = "openai"
    state_in_cloud: bool = True
    tools_in_cloud: bool = True
    loop_in_cloud: bool = True
    def migration_cost(self, target: str) -> dict:
        if target == self.platform:
            return {"cost_lines": 30, "note": "同平台升级 轻适配"}
        return {"cost_lines": 280, "note": "跨平台重写 Threads导出+function适配+loop自研",
                "state": "重写", "tools": "重写", "loop": "重写"}

@dataclass
class AbstractedVendorLock:
    """抽象层托管: LiteLLM统一API + 本地镜像state + 开标协议tools"""
    abstraction: str = "LiteLLM"
    state_local_mirror: bool = True
    tools_open_protocol: bool = True
    latency_ms: int = 200
    lag_weeks: int = 3
    def migration_cost(self, target: str) -> dict:
        if target == "openai":
            return {"cost_lines": 50, "note": "同平台 抽象层适配",
                    "latency_ms": self.latency_ms, "lag_weeks": self.lag_weeks}
        return {"cost_lines": 80, "note": "跨平台 抽象层改适配 + 本地数据迁移",
                "state": "本地镜像迁移", "tools": "开标协议复用", "loop": "抽象层适配"}

@dataclass
class NativeWithMirror:
    """原生API + 本地镜像(甜点): 保新功能 + 数据有底"""
    state_local_mirror: bool = True
    tools_open_protocol: bool = True
    def migration_cost(self, target: str) -> dict:
        if target == "openai":
            return {"cost_lines": 30, "note": "原生API轻适配"}
        return {"cost_lines": 120, "note": "跨平台 原生重写适配层 + 本地数据迁移",
                "state": "本地镜像迁移", "tools": "开标协议复用", "loop": "自研重写"}

def main():
    """demo: 裸锁定 vs LiteLLM抽象层 vs 原生+本地镜像"""
    print("=" * 60)
    print("托管锁锁定: 裸锁定 vs LiteLLM vs 原生+本地镜像")
    print("=" * 60)
    naive = NaiveVendorLock()
    abstracted = AbstractedVendorLock()
    native = NativeWithMirror()
    print(f"{'切换场景':<20} {'裸锁定':<14} {'LiteLLM':<14} {'原生+镜像':<14}")
    print("-" * 60)
    for target, label in [("openai", "OpenAI内升级"), ("anthropic", "切到Anthropic"), ("self", "切到自研")]:
        n = naive.migration_cost(target)
        a = abstracted.migration_cost(target)
        nv = native.migration_cost(target)
        print(f"{label:<20} {n['cost_lines']}行{'':<9} {a['cost_lines']}行{'':<9} {nv['cost_lines']}行")
    print("\n" + "-" * 60)
    print("抽象层代价:")
    print(f"  LiteLLM: 延迟+{abstracted.latency_ms}ms/调用 + 新API滞后{abstracted.lag_weeks}周")
    print(f"  原生+镜像: 保新功能 + 数据有底 但切换120行")
    print("=" * 60)
    print("结论: 裸锁定切换280行, LiteLLM抽象层80行(但延迟+200ms/滞后3周),")
    print("      原生+本地镜像120行(甜点 保新功能+数据有底)")
    print("      开标协议tools(MCP)需写适配层60行 是2.14篇展开点")

if __name__ == "__main__":
    main()
