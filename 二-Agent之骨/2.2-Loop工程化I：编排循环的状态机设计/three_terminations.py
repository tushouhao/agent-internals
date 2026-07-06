# 文件名: three_terminations.py
# 功能: 三类终止条件（成功/失败/熔断）的下游处置
# 运行: python three_terminations.py

"""三类终止条件：完成不等于成功。

成功终止: 产物归档/成本结算/轨迹入记忆
失败终止: 诊断报告/部分产物保留/轨迹入记忆（带失败标记）
熔断终止: 告警通知/产物冻结/轨迹入审计
教学版，模拟三类终止的处置流水。
"""
from dataclasses import dataclass
from collections import Counter
import random

random.seed(2026)

@dataclass
class TraceRecord:
    step: int
    state: str
    tool: str
    result: str

@dataclass
class DiagnosticReport:
    fail_step: int
    fail_tool: str
    fail_args: dict
    last_success_observe: str
    total_steps: int

def classify_termination(final_state: str, ctx: dict) -> str:
    """根据最终态分类终止类型。"""
    if final_state == "finish":
        return "成功"
    if final_state in ("escalate", "abort") and ctx.get("budget_exceeded"):
        return "熔断"
    return "失败"

def success_postprocess(artifacts: list[str], cost: float,
                        traces: list[TraceRecord]) -> dict:
    """成功终止处置。"""
    return {
        "归档产物": [f"v{i}_{a}" for i, a in enumerate(artifacts)],
        "成本结算": f"${cost:.2f}",
        "轨迹入记忆": f"{len(traces)} 步成功轨迹",
    }

def failure_postprocess(artifacts: list[str], traces: list[TraceRecord],
                        fail_step: int) -> DiagnosticReport:
    """失败终止处置。"""
    last_success = next(
        (t.result for t in reversed(traces[:fail_step]) if "ok" in t.result),
        "无成功观察"
    )
    return DiagnosticReport(
        fail_step=fail_step,
        fail_tool=traces[fail_step-1].tool if fail_step <= len(traces) else "unknown",
        fail_args={"path": "/tmp/fail.txt"},
        last_success_observe=last_success,
        total_steps=len(traces),
    )

def breaker_postprocess(ctx: dict, traces: list[TraceRecord]) -> dict:
    """熔断终止处置。"""
    return {
        "告警通知": "slack + email 已发",
        "产物冻结": "冻结现场，不归档",
        "轨迹入审计": f"{len(traces)} 步写入审计日志（不可篡改）",
        "熔断原因": ctx.get("break_reason", "未知"),
    }

def simulate_runs(trials: int) -> Counter:
    """模拟 trials 次任务的终止类型分布。"""
    results = Counter()
    for _ in range(trials):
        r = random.random()
        if r < 0.78:
            results["成功"] += 1
        elif r < 0.93:
            results["失败"] += 1
        else:
            results["熔断"] += 1
    return results

def main():
    print("=" * 64)
    print("三类终止条件：下游处置对比")
    print("=" * 64)
    # 模拟分布
    dist = simulate_runs(1000)
    print("\n生产终止类型分布（1000 次模拟）:")
    for k, v in dist.most_common():
        print(f"  {k}: {v} ({v/10:.0%})")

    # 成功处置 demo
    print("\n【成功终止】处置:")
    ok = success_postprocess(["report.md", "data.csv"], 2.34,
                             [TraceRecord(1, "act", "read", "ok")])
    for k, v in ok.items():
        print(f"  {k}: {v}")

    # 失败处置 demo
    print("\n【失败终止】处置:")
    traces = [TraceRecord(1, "act", "read", "ok: 内容"),
              TraceRecord(2, "act", "write", "error: 磁盘满")]
    fail = failure_postprocess(["draft.md"], traces, fail_step=2)
    print(f"  诊断报告: 失败步={fail.fail_step}, 工具={fail.fail_tool}")
    print(f"  部分产物: draft.md 保留")
    print(f"  轨迹入记忆: 带失败标记")

    # 熔断处置 demo
    print("\n【熔断终止】处置:")
    brk = breaker_postprocess({"break_reason": "预算超限"}, traces)
    for k, v in brk.items():
        print(f"  {k}: {v}")

    print("\n结论：三类终止的下游处置完全不同，")
    print("      告警对熔断态响应时延应 < 30 秒。")

if __name__ == "__main__":
    main()
