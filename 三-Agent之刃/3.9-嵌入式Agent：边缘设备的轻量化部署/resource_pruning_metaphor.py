"""
第1章源码：资源三阶裁剪隐喻——三阶部署参数形式化
演示三阶架构的四轴外扩参数表
"""


def define_three_stages() -> dict:
    """定义三阶裁剪架构参数"""
    stages = {
        "云端全量阶": {
            "model_params": "7B",
            "memory_usage": "16GB VRAM",
            "inference_latency_ms": 200,
            "capability_coverage": 1.00,
            "crash_mode": "网络断即停",
            "deployment_target": "云端 GPU",
        },
        "本地裁剪阶": {
            "model_params": "1.5B",
            "memory_usage": "1.5GB RAM",
            "inference_latency_ms": 500,
            "capability_coverage": 0.75,
            "crash_mode": "量化精度损失",
            "deployment_target": "边缘 NPU",
        },
        "微端即用阶": {
            "model_params": "300M",
            "memory_usage": "256MB RAM",
            "inference_latency_ms": 50,
            "capability_coverage": 0.40,
            "crash_mode": "蒸馏能力天花板",
            "deployment_target": "微控制器",
        },
    }
    return stages


def stage_evolution_trace() -> list[dict]:
    """生成三阶演进追踪数据——四轴外扩幅度"""
    metrics = ["inference_latency_ms", "capability_coverage"]
    stages = define_three_stages()
    trace = []
    names = ["云端全量阶", "本地裁剪阶", "微端即用阶"]
    for i, name in enumerate(names):
        row = {"stage": name, "evolution_step": i}
        for m in metrics:
            row[m] = stages[name][m]
        trace.append(row)
    return trace


if __name__ == "__main__":
    stages = define_three_stages()
    trace = stage_evolution_trace()

    print("=" * 56)
    print("资源三阶裁剪隐喻 — 三阶部署架构参数")
    print("=" * 56)
    for name, params in stages.items():
        print(f"\n  [{name}]")
        print(f"    模型参数: {params['model_params']}")
        print(f"    显存占用: {params['memory_usage']}")
        print(f"    推理延迟: {params['inference_latency_ms']}ms")
        print(f"    能力覆盖: {params['capability_coverage']:.0%}")
        print(f"    崩溃模式: {params['crash_mode']}")
        print(f"    部署目标: {params['deployment_target']}")

    print("\n" + "=" * 56)
    print("四轴外扩追踪")
    print("=" * 56)
    for row in trace:
        print(f"  {row['stage']:>8s} | step={row['evolution_step']} | "
              f"latency={row['inference_latency_ms']:>4d}ms | "
              f"coverage={row['capability_coverage']:.0%}")
