"""
第3章源码：服务池态——多实例负载均衡与资源争用管理
模拟轮询调度+令牌桶限流+熔断
"""

import time
import random


class TokenBucket:
    """令牌桶——API 配额限流"""

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # 每秒补充
        self.last_refill = time.time()

    def acquire(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


class AgentInstance:
    """Agent 实例——服务池中的工作进程"""

    def __init__(self, instance_id: int):
        self.instance_id = instance_id
        self.active_connections = 0
        self.total_processed = 0
        self.errors = 0
        self.alive = True

    def process(self, request: dict) -> dict:
        if not self.alive:
            return {"status": "dead"}
        self.active_connections += 1
        self.total_processed += 1
        latency = 0.05 + random.random() * 0.15
        time.sleep(latency * 0.1)  # 模拟处理
        # 模拟随机故障
        if random.random() < 0.05:
            self.errors += 1
            self.active_connections -= 1
            return {"status": "error", "instance": self.instance_id}
        self.active_connections -= 1
        return {
            "status": "ok", "instance": self.instance_id,
            "latency": round(latency, 3),
            "result": f"req processed by instance-{self.instance_id}"
        }


class ServicePool:
    """服务池——多实例负载均衡"""

    def __init__(self, num_instances: int = 4):
        self.instances = [AgentInstance(i) for i in range(num_instances)]
        self.counter = 0  # 轮询计数器
        self.token_bucket = TokenBucket(capacity=10, refill_rate=5)
        self.circuit_breaker_open = False
        self.error_threshold = 0.3

    def round_robin(self) -> AgentInstance | None:
        """轮询调度——选择下一个存活实例"""
        for _ in range(len(self.instances)):
            self.counter = (self.counter + 1) % len(self.instances)
            inst = self.instances[self.counter]
            if inst.alive:
                return inst
        return None

    def health_check(self):
        """健康检查——重建死亡实例"""
        for i, inst in enumerate(self.instances):
            if not inst.alive or (inst.active_connections > 0
                                  and inst.errors / max(inst.total_processed, 1) > 0.5):
                print(f"  [health] instance-{i} 死亡, 重建")
                self.instances[i] = AgentInstance(i)

    def process_request(self, request: dict) -> dict:
        """处理请求——含限流和熔断"""
        if self.circuit_breaker_open:
            return {"status": "circuit_breaker", "result": "降级: 服务暂不可用"}

        if not self.token_bucket.acquire():
            return {"status": "rate_limited", "result": "限流: API 配额耗尽"}

        instance = self.round_robin()
        if not instance:
            return {"status": "no_instances", "result": "无可用实例"}

        result = instance.process(request)

        # 熔断检测
        total_errors = sum(i.errors for i in self.instances)
        total_processed = sum(i.total_processed for i in self.instances)
        if total_processed > 10:
            error_rate = total_errors / total_processed
            if error_rate > self.error_threshold:
                self.circuit_breaker_open = True
                print(f"  [熔断] 错误率 {error_rate:.0%} 超过阈值 {self.error_threshold:.0%}")

        self.health_check()
        return result


def run_pool_test(pool: ServicePool, num_requests: int = 30) -> list[dict]:
    results = []
    for i in range(num_requests):
        req = {"prompt": f"request-{i}"}
        resp = pool.process_request(req)
        results.append({"req_id": i, **resp})
    return results


if __name__ == "__main__":
    pool = ServicePool(num_instances=4)
    print("=" * 56)
    print("服务池态 — 多实例负载均衡压测")
    print("=" * 56)
    results = run_pool_test(pool, 30)

    status_counts = {}
    for r in results:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        print(f"  req#{r['req_id']:>2d} | {r['status']:>15s} | "
              f"instance={str(r.get('instance', '-')):>3s} | "
              f"latency={r.get('latency', '-')}")

    print(f"\n  状态分布: {status_counts}")
    total_processed = sum(i.total_processed for i in pool.instances)
    total_errors = sum(i.errors for i in pool.instances)
    print(f"  实例总计: processed={total_processed} errors={total_errors}")
    print(f"  熔断状态: {'开启' if pool.circuit_breaker_open else '关闭'}")
