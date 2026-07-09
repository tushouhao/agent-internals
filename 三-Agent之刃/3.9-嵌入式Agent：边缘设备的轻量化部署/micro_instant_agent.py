"""
第4章源码：微端即用阶——蒸馏小模型与硬实时部署
模拟 7B→300M 蒸馏 + INT4 量化 + 50ms 硬实时推理
"""

import random
import time


class KnowledgeDistiller:
    """知识蒸馏器——7B→300M"""

    def __init__(self):
        self.teacher_params = 7_000_000_000
        self.student_params = 300_000_000
        self.distilled_tasks = []

    def distill(self, teacher_tasks: list[str], frequency_threshold: int = 5) -> list[str]:
        """蒸馏——按任务频次保留核心能力"""
        # 模拟频次统计
        task_freq = {t: random.randint(1, 10) for t in teacher_tasks}
        retained = [t for t, f in task_freq.items() if f >= frequency_threshold]
        self.distilled_tasks = retained
        # 模拟能力覆盖
        coverage = len(retained) / max(len(teacher_tasks), 1)
        return retained

    def compression_ratio(self) -> float:
        return self.teacher_params / self.student_params


class INT4Quantizer:
    """INT4 极限量化器"""

    def __init__(self):
        self.int8_size_mb = 1500
        self.int4_size_mb = 750
        self.precision_loss = 0.0
        self.capability_ceiling = 0.40  # 能力天花板

    def quantize(self, weights: dict) -> dict:
        """模拟 INT4 量化——截断到 16 级"""
        quantized = {}
        for key, value in weights.items():
            if isinstance(value, list):
                max_val = max(abs(v) for v in value) if value else 1.0
                scale = max_val / 7 if max_val > 0 else 1.0
                quantized[key] = [round(v / scale) * scale for v in value]
            else:
                quantized[key] = value
        self.precision_loss = random.uniform(0.15, 0.25)
        return quantized

    def memory_saving(self) -> float:
        return 1 - self.int4_size_mb / self.int8_size_mb


class MicroRealTimeEngine:
    """微端硬实时推理引擎"""

    def __init__(self, quantizer: INT4Quantizer):
        self.quantizer = quantizer
        self.loaded = False
        self.inference_count = 0
        self.deadline_ms = 50  # 硬实时截止
        self.supported_tasks: list[str] = []

    def load(self, weights: dict, supported_tasks: list[str]):
        quantized = self.quantizer.quantize(weights)
        self.loaded = True
        self.supported_tasks = supported_tasks

    def infer(self, task: str, prompt: str) -> dict:
        if not self.loaded:
            return {"status": "not_loaded"}
        self.inference_count += 1

        # 任务能力检查
        if task not in self.supported_tasks:
            return {"status": "unsupported", "reason": f"任务 {task} 未蒸馏"}

        # 硬实时推理
        latency = 0.03 + random.random() * 0.02  # 30-50ms
        time.sleep(latency * 0.01)
        deadline_met = latency * 1000 <= self.deadline_ms

        if not deadline_met:
            return {"status": "deadline_miss", "latency_ms": round(latency * 1000)}

        result = f"micro_inferred: {prompt[:15]}..."
        return {
            "status": "ok", "result": result,
            "latency_ms": round(latency * 1000),
            "precision_loss": round(self.quantizer.precision_loss, 3),
        }


class MicroInstantAgent:
    """微端即用 Agent——蒸馏 + INT4 + 硬实时"""

    def __init__(self):
        self.distiller = KnowledgeDistiller()
        self.quantizer = INT4Quantizer()
        self.engine = MicroRealTimeEngine(self.quantizer)
        self.weights = {"layer1": [0.1, 0.5, 0.3], "layer2": [0.2, 0.8]}

    def deploy(self, all_tasks: list[str]):
        retained = self.distiller.distill(all_tasks)
        self.engine.load(self.weights, retained)

    def process(self, task: str, prompt: str) -> dict:
        if not self.engine.loaded:
            self.deploy(["温度读取", "开关控制", "状态查询", "复杂分析", "报表生成"])
        return self.engine.infer(task, prompt)


def run_micro_agent_test(agent: MicroInstantAgent, num_requests: int = 25) -> list[dict]:
    results = []
    task_pool = [
        ("温度读取", "temp sensor"), ("开关控制", "toggle valve"),
        ("状态查询", "device status"), ("复杂分析", "deep analysis"),
        ("报表生成", "monthly report"),
    ]
    for i in range(num_requests):
        task, prompt = task_pool[i % 5]
        result = agent.process(task, prompt)
        results.append({"req_id": i, "task": task, **result})
    return results


if __name__ == "__main__":
    agent = MicroInstantAgent()
    print("=" * 56)
    print("微端即用阶 — 蒸馏 + INT4 + 硬实时压测")
    print("=" * 56)
    agent.deploy(["温度读取", "开关控制", "状态查询", "复杂分析", "报表生成"])
    print(f"  蒸馏压缩比: {agent.distiller.compression_ratio():.1f}x")
    print(f"  蒸馏保留任务: {agent.distiller.distilled_tasks}")
    print(f"  INT4 内存节省: {agent.quantizer.memory_saving():.1%}")
    print(f"  初始精度损失: {agent.quantizer.precision_loss:.3f}")
    print(f"  能力天花板: {agent.quantizer.capability_ceiling:.0%}")

    results = run_micro_agent_test(agent, 25)
    status_counts = {}
    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        print(f"  req#{r['req_id']:>2d} | {r['task']:>6s} | {r['status']:>14s} | "
              f"latency={r.get('latency_ms', '-'):}ms")

    print(f"\n  状态分布: {status_counts}")
    print(f"  推理次数: {agent.engine.inference_count}")
    print(f"  支持任务: {agent.engine.supported_tasks}")
