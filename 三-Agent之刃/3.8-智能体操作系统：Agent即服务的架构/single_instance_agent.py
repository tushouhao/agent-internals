"""
第2章源码：单实例态——无状态 Agent 服务封装
模拟单 Agent 串行处理多个请求，含资源监控
"""

import time
import random


class AgentService:
    """单实例 Agent 服务——无状态串行处理"""

    def __init__(self, model_name: str = "mock-llm"):
        self.model_name = model_name
        self.memory_used_mb = 0
        self.total_requests = 0
        self.timeouts = 0
        self.oom_count = 0

    def process(self, request: dict) -> dict:
        """处理单个请求——模拟 LLM 推理"""
        self.total_requests += 1
        prompt = request.get("prompt", "")
        max_tokens = request.get("max_tokens", 100)

        # 模拟推理耗时
        latency = 0.05 + random.random() * 0.1
        if latency > 0.13:  # 模拟超时
            self.timeouts += 1
            time.sleep(0.01)
            return {"status": "timeout", "latency": latency}

        # 模拟内存增长
        simulated_memory = len(prompt) * 0.01 + max_tokens * 0.005
        self.memory_used_mb += simulated_memory

        if self.memory_used_mb > 500:  # 模拟 OOM
            self.oom_count += 1
            self.memory_used_mb = 0  # 重置
            time.sleep(0.01)
            return {"status": "oom", "latency": latency}

        time.sleep(latency * 0.1)  # 默认采样加速
        result = f"processed: {prompt[:20]}... ({max_tokens} tokens)"
        return {"status": "ok", "result": result, "latency": round(latency, 3)}

    def health(self) -> dict:
        """健康检查"""
        return {
            "model": self.model_name,
            "total_requests": self.total_requests,
            "memory_mb": round(self.memory_used_mb, 1),
            "timeouts": self.timeouts,
            "oom_count": self.oom_count,
        }


def run_stress_test(service: AgentService, num_requests: int = 20) -> list[dict]:
    """串行压测"""
    results = []
    prompts = [
        "查询用户订单历史" if i % 3 == 0 else
        "生成周报摘要" if i % 3 == 1 else
        "分析销售趋势图"
        for i in range(num_requests)
    ]
    for i in range(num_requests):
        req = {"prompt": prompts[i], "max_tokens": 50 + (i % 5) * 50}
        resp = service.process(req)
        results.append({"req_id": i, **resp})
    return results


if __name__ == "__main__":
    service = AgentService()
    print("=" * 56)
    print("单实例态 — Agent 服务串行压测")
    print("=" * 56)
    results = run_stress_test(service, 20)
    ok_count = sum(1 for r in results if r["status"] == "ok")
    timeout_count = sum(1 for r in results if r["status"] == "timeout")
    oom_count = sum(1 for r in results if r["status"] == "oom")

    for r in results:
        print(f"  req#{r['req_id']:>2d} | {r['status']:>7s} | "
              f"latency={r.get('latency', '-'):>.3f}s")

    print(f"\n  总计: {len(results)} | ok={ok_count} | "
          f"timeout={timeout_count} | oom={oom_count}")
    print(f"  健康: {service.health()}")
