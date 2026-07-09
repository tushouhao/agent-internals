"""
第2章源码：云端全量阶——重模型远程调用与离线降级
模拟边缘设备转发请求到云端 + LRU 缓存 + 离线降级
"""

import time
import random
from collections import OrderedDict


class LRUCache:
    """LRU 缓存——边缘结果落地"""

    def __init__(self, capacity: int = 50):
        self.capacity = capacity
        self.cache: OrderedDict[str, dict] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> dict | None:
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key: str, value: dict):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class CloudInference:
    """云端推理——模拟 7B 模型远程调用"""

    def __init__(self):
        self.total_calls = 0
        self.network_available = True

    def infer(self, prompt: str) -> dict:
        self.total_calls += 1
        if not self.network_available:
            return {"status": "offline", "reason": "网络断开"}
        # 模拟云端推理延迟
        latency = 0.15 + random.random() * 0.1  # 150-250ms
        time.sleep(latency * 0.01)  # 压缩模拟时间
        result = f"cloud_inferred: {prompt[:20]}..."
        return {"status": "ok", "result": result, "latency_ms": round(latency * 1000)}

    def toggle_network(self, available: bool):
        self.network_available = available


class EdgeCloudAgent:
    """边缘云端 Agent——转发 + 缓存 + 降级"""

    def __init__(self):
        self.cloud = CloudInference()
        self.cache = LRUCache(capacity=20)
        self.degradation_template = {
            "default": "降级响应：网络不可用，请稍后重试",
            "faq": "降级响应：常见问题请查阅本地手册",
        }
        self.total_requests = 0
        self.degraded_count = 0

    def process(self, prompt: str, task_type: str = "default") -> dict:
        self.total_requests += 1
        # 先查缓存
        cached = self.cache.get(prompt)
        if cached:
            return {**cached, "source": "cache"}

        # 云端推理
        result = self.cloud.infer(prompt)
        if result["status"] == "ok":
            self.cache.put(prompt, result)
            return {**result, "source": "cloud"}

        # 离线降级
        self.degraded_count += 1
        return {
            "status": "degraded",
            "result": self.degradation_template.get(task_type, self.degradation_template["default"]),
            "source": "degradation",
        }


def run_cloud_agent_test(agent: EdgeCloudAgent, num_requests: int = 30) -> list[dict]:
    """压测云端全量阶——含网络断开场景"""
    results = []
    prompts = [f"query-{i}" for i in range(num_requests)]
    task_types = ["default", "faq", "default"]

    for i in range(num_requests):
        # 第 10 个请求后断网，第 20 个请求后恢复
        if i == 10:
            agent.cloud.toggle_network(False)
        elif i == 20:
            agent.cloud.toggle_network(True)

        # 重复请求测试缓存
        if i >= 5 and i < 10:
            prompt = prompts[i - 5]  # 重复前 5 个
        else:
            prompt = prompts[i]

        result = agent.process(prompt, task_types[i % 3])
        results.append({"req_id": i, "prompt": prompt, **result})
    return results


if __name__ == "__main__":
    agent = EdgeCloudAgent()
    print("=" * 56)
    print("云端全量阶 — 边缘转发 + 缓存 + 降级压测")
    print("=" * 56)
    results = run_cloud_agent_test(agent, 30)

    source_counts = {}
    for r in results:
        source_counts[r["source"]] = source_counts.get(r["source"], 0) + 1
        print(f"  req#{r['req_id']:>2d} | {r['source']:>11s} | "
              f"status={r['status']:>8s} | latency={r.get('latency_ms', '-')}")

    print(f"\n  来源分布: {source_counts}")
    print(f"  缓存命中率: {agent.cache.hit_rate():.1%}")
    print(f"  云端调用数: {agent.cloud.total_calls}")
    print(f"  降级次数: {agent.degraded_count}")
