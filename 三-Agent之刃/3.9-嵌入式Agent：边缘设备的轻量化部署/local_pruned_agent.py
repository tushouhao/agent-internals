"""
第3章源码：本地裁剪阶——量化压缩与离线推理
模拟 7B→1.5B 裁剪 + FP16→INT8 量化 + 精度校准
"""

import random


class ModelPruner:
    """模型裁剪器——7B→1.5B"""

    def __init__(self):
        self.original_params = 7_000_000_000
        self.pruned_params = 1_500_000_000

    def prune(self, model_weights: dict) -> dict:
        """模拟剪枝——保留重要权重"""
        pruned = {}
        for key, value in model_weights.items():
            # 模拟剪枝：保留权重绝对值大的
            if isinstance(value, list):
                retained = [v for v in value if abs(v) > 0.01]
                pruned[key] = retained if retained else [0.0]
            else:
                pruned[key] = value
        return pruned

    def compression_ratio(self) -> float:
        return self.original_params / self.pruned_params


class Quantizer:
    """量化器——FP16→INT8"""

    def __init__(self):
        self.fp16_size_mb = 3000  # 1.5B 模型 FP16 约 3GB
        self.int8_size_mb = 1500  # INT8 约 1.5GB
        self.precision_loss = 0.0

    def quantize(self, weights: dict) -> dict:
        """模拟 INT8 量化——截断精度"""
        quantized = {}
        for key, value in weights.items():
            if isinstance(value, list):
                # 模拟 INT8：量化到 256 级
                max_val = max(abs(v) for v in value) if value else 1.0
                scale = max_val / 127 if max_val > 0 else 1.0
                quantized[key] = [round(v / scale) * scale for v in value]
            else:
                quantized[key] = value
        # 模拟精度损失
        self.precision_loss = random.uniform(0.02, 0.08)
        return quantized

    def memory_saving(self) -> float:
        return 1 - self.int8_size_mb / self.fp16_size_mb


class LocalInferenceEngine:
    """本地推理引擎——边缘 NPU 推理"""

    def __init__(self, quantizer: Quantizer):
        self.quantizer = quantizer
        self.loaded = False
        self.inference_count = 0
        self.precision_threshold = 0.05  # 精度误差阈值

    def load_model(self, weights: dict):
        """加载量化模型到边缘设备"""
        quantized = self.quantizer.quantize(weights)
        self.loaded = True
        return quantized

    def infer(self, prompt: str, cloud_reference: str | None = None) -> dict:
        """本地推理——含精度校准"""
        if not self.loaded:
            return {"status": "not_loaded"}
        self.inference_count += 1
        # 模拟边缘推理
        latency = 0.4 + random.random() * 0.2  # 400-600ms
        result = f"local_inferred: {prompt[:20]}..."

        # 精度校准
        if cloud_reference:
            error = self.quantizer.precision_loss
            if error > self.precision_threshold:
                return {
                    "status": "precision_fallback",
                    "result": "精度不足，回退云端",
                    "error": round(error, 3),
                }

        return {
            "status": "ok", "result": result,
            "latency_ms": round(latency * 1000),
            "precision_loss": round(self.quantizer.precision_loss, 3),
        }


class LocalPrunedAgent:
    """本地裁剪 Agent——裁剪 + 量化 + 推理 + 校准"""

    def __init__(self):
        self.pruner = ModelPruner()
        self.quantizer = Quantizer()
        self.engine = LocalInferenceEngine(self.quantizer)
        self.weights = {"layer1": [0.1, 0.05, 0.3, 0.002, 0.8], "layer2": [0.2, 0.01, 0.5]}

    def deploy(self):
        """部署流程：裁剪 → 量化 → 加载"""
        pruned = self.pruner.prune(self.weights)
        self.engine.load_model(pruned)

    def process(self, prompt: str, cloud_ref: str | None = None) -> dict:
        if not self.engine.loaded:
            self.deploy()
        return self.engine.infer(prompt, cloud_ref)


def run_local_agent_test(agent: LocalPrunedAgent, num_requests: int = 20) -> list[dict]:
    results = []
    for i in range(num_requests):
        prompt = f"local-query-{i}"
        # 每 5 个请求提供云端参考做精度校准
        cloud_ref = f"cloud_ref-{i}" if i % 5 == 0 else None
        result = agent.process(prompt, cloud_ref)
        results.append({"req_id": i, **result})
    return results


if __name__ == "__main__":
    agent = LocalPrunedAgent()
    print("=" * 56)
    print("本地裁剪阶 — 量化压缩 + 离线推理压测")
    print("=" * 56)
    agent.deploy()
    print(f"  裁剪压缩比: {agent.pruner.compression_ratio():.1f}x")
    print(f"  量化内存节省: {agent.quantizer.memory_saving():.1%}")
    print(f"  初始精度损失: {agent.quantizer.precision_loss:.3f}")

    results = run_local_agent_test(agent, 20)
    status_counts = {}
    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        print(f"  req#{r['req_id']:>2d} | {r['status']:>18s} | "
              f"latency={r.get('latency_ms', '-'):}ms | "
              f"loss={r.get('precision_loss', r.get('error', '-'))}")

    print(f"\n  状态分布: {status_counts}")
    print(f"  推理次数: {agent.engine.inference_count}")
