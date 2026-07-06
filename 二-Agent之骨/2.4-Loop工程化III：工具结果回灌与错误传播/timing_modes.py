# 文件名: timing_modes.py
# 功能: 回灌时序——同步、异步、流式三模式
# 运行: python timing_modes.py

"""回灌的时序：同步、异步、流式。

同步: 快工具（<1s）, loop 阻塞等结果, 一次性回灌
异步: 慢工具（>30s）, 后台跑, 立即回灌 task_id, 完成时回调
流式: 进度工具, 边跑边产部分结果, 每 N 秒回灌一次
生产 loop 必须三种都支持, 只支持同步会在慢工具上阻塞崩溃。
教学版，模拟三种时序。
"""
import time
from dataclasses import dataclass, field

@dataclass
class SyncResult:
    tool: str
    elapsed_ms: int
    tokens: int

@dataclass
class AsyncResult:
    task_id: str
    tool: str
    status: str = "running"      # running / done / failed
    result_tokens: int = 0
    elapsed_ms: int = 0
    critical: bool = False        # finish 时是否等

@dataclass
class StreamingResult:
    tool: str
    partial_chunks: list[dict] = field(default_factory=list)
    progress: float = 0.0         # 0-1
    final_summary_tokens: int = 0

def sync_demo() -> SyncResult:
    return SyncResult("read_file", 50, 5000)

def async_demo() -> AsyncResult:
    return AsyncResult("task_abc", "train_model", critical=True)

def streaming_demo() -> StreamingResult:
    return StreamingResult("analyze_logs",
                           [{"chunk": i, "tokens": 500, "partial": True} for i in range(5)],
                           progress=1.0, final_summary_tokens=200)

def main():
    print("=" * 64)
    print("回灌时序：同步 / 异步 / 流式")
    print("=" * 64)
    print("\n【同步回灌】（快工具, 85% 占比）:")
    s = sync_demo()
    print(f"  工具: {s.tool}, 耗时: {s.elapsed_ms}ms, 回灌: {s.tokens}t 一次性")

    print("\n【异步回灌】（慢工具, 10% 占比）:")
    a = async_demo()
    print(f"  工具: {a.tool}, task_id: {a.task_id}")
    print(f"  立即回灌: task_id（让模型知有后台任务）")
    print(f"  完成时回灌: 200t 结果, critical={a.critical}（finish 时等）")

    print("\n【流式回灌】（进度工具, 5% 占比）:")
    st = streaming_demo()
    print(f"  工具: {st.tool}")
    print(f"  部分回灌: {len(st.partial_chunks)} 次, 每次 {st.partial_chunks[0]['tokens']}t")
    print(f"  部分结果标 partial=true, 模型不能当全量")
    print(f"  完成时回灌: {st.final_summary_tokens}t 汇总")
    print()
    print("结论: naive 只支持同步, 慢工具阻塞 loop 10 分钟")
    print("      finish 前等异步: critical 等, 非critical 丢弃 + 告警")

if __name__ == "__main__":
    main()
