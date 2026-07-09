"""
第1章源码：进程三态调度隐喻——三态定义与架构参数形式化
演示三态架构的四轴外扩参数表，非第1章内容但仍提供可运行验证
"""


def define_three_tiers() -> dict:
    """定义三态架构参数"""
    tiers = {
        "单实例态": {
            "concurrency": 1,
            "resource_contention": "无",
            "scheduling": "先来先服务",
            "isolation": "无",
            "crash_mode": "OOM/超时无后备",
            "throughput_qps": 1.0,
        },
        "服务池态": {
            "concurrency": 10,
            "resource_contention": "API 配额争用",
            "scheduling": "轮询/最少连接",
            "isolation": "进程隔离",
            "crash_mode": "资源耗尽+雪崩",
            "throughput_qps": 8.5,
        },
        "调度系统态": {
            "concurrency": 100,
            "resource_contention": "全局资源调度",
            "scheduling": "优先级+配额+抢占",
            "isolation": "资源配额隔离+熔断",
            "crash_mode": "优先级反转+死锁",
            "throughput_qps": 75.0,
        },
    }
    return tiers


def tier_evolution_trace() -> list[dict]:
    """生成三态演进追踪数据——四轴外扩幅度"""
    metrics = ["concurrency", "throughput_qps"]
    tiers = define_three_tiers()
    trace = []
    names = ["单实例态", "服务池态", "调度系统态"]
    for i, name in enumerate(names):
        row = {"tier": name, "evolution_step": i}
        for m in metrics:
            row[m] = tiers[name][m]
        trace.append(row)
    return trace


if __name__ == "__main__":
    tiers = define_three_tiers()
    trace = tier_evolution_trace()

    print("=" * 56)
    print("进程三态调度隐喻 — 三态架构参数")
    print("=" * 56)
    for name, params in tiers.items():
        print(f"\n  [{name}]")
        print(f"    并发数: {params['concurrency']}")
        print(f"    资源争用: {params['resource_contention']}")
        print(f"    调度策略: {params['scheduling']}")
        print(f"    隔离级别: {params['isolation']}")
        print(f"    崩溃模式: {params['crash_mode']}")
        print(f"    吞吐量(QPS): {params['throughput_qps']}")

    print("\n" + "=" * 56)
    print("四轴外扩追踪")
    print("=" * 56)
    for row in trace:
        print(f"  {row['tier']:>8s} | step={row['evolution_step']} | "
              f"concurrency={row['concurrency']:>3d} | "
              f"QPS={row['throughput_qps']:>5.1f}")
