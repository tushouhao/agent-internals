"""
第5章源码：混合部署调度——云端兜底 + 边缘优先
模拟三阶裁剪按任务复杂度分流 + 断网守护
"""

import random
import time


class EdgeTierHandler:
    """边缘阶处理器——本地裁剪阶能力"""
    EDGE_CAPABLE = {"温度读取", "开关控制", "状态查询"}

    def __init__(self):
        self.handled = 0
        self.fallback_count = 0

    def can_handle(self, task: str) -> bool:
        return task in self.EDGE_CAPABLE

    def handle(self, task: str, prompt: str) -> dict:
        self.handled += 1
        latency = 0.4 + random.random() * 0.2
        time.sleep(latency * 0.01)
        return {
            "tier": "edge", "task": task, "status": "ok",
            "latency_ms": round(latency * 1000),
            "result": f"edge: {prompt[:15]}",
        }


class MicroTierHandler:
    """微端阶处理器——硬实时能力"""
    MICRO_CAPABLE = {"温度读取", "开关控制"}

    def __init__(self):
        self.handled = 0
        self.deadline_miss = 0

    def can_handle(self, task: str) -> bool:
        return task in self.MICRO_CAPABLE

    def handle(self, task: str, prompt: str) -> dict:
        self.handled += 1
        latency = 0.03 + random.random() * 0.02
        time.sleep(latency * 0.01)
        if latency * 1000 > 50:
            self.deadline_miss += 1
            return {"tier": "micro", "task": task, "status": "deadline_miss"}
        return {
            "tier": "micro", "task": task, "status": "ok",
            "latency_ms": round(latency * 1000),
            "result": f"micro: {prompt[:15]}",
        }


class CloudTierHandler:
    """云端阶处理器——全量能力兜底"""

    def __init__(self):
        self.handled = 0
        self.network_available = True

    def can_handle(self, task: str) -> bool:
        return self.network_available  # 云端能处理所有任务，但依赖网络

    def handle(self, task: str, prompt: str) -> dict:
        if not self.network_available:
            return {"tier": "cloud", "task": task, "status": "offline"}
        self.handled += 1
        latency = 0.15 + random.random() * 0.1
        time.sleep(latency * 0.01)
        return {
            "tier": "cloud", "task": task, "status": "ok",
            "latency_ms": round(latency * 1000),
            "result": f"cloud: {prompt[:15]}",
        }

    def toggle_network(self, available: bool):
        self.network_available = available


class HybridDeploymentRouter:
    """混合部署调度器——微端优先 → 边缘次选 → 云端兜底"""

    def __init__(self):
        self.micro = MicroTierHandler()
        self.edge = EdgeTierHandler()
        self.cloud = CloudTierHandler()
        self.router_log: list[tuple[int, str]] = []
        self.reject_count = 0

    def route(self, task: str, prompt: str) -> dict:
        req_id = len(self.router_log)
        # 优先级：微端 → 边缘 → 云端
        if self.micro.can_handle(task):
            self.router_log.append((req_id, "micro"))
            return self.micro.handle(task, prompt)
        elif self.edge.can_handle(task):
            self.router_log.append((req_id, "edge"))
            return self.edge.handle(task, prompt)
        elif self.cloud.can_handle(task):
            self.router_log.append((req_id, "cloud"))
            result = self.cloud.handle(task, prompt)
            if result["status"] == "offline":
                self.reject_count += 1
                return {"tier": "rejected", "task": task, "status": "reject",
                        "reason": "断网且边缘无能力"}
            return result
        else:
            self.reject_count += 1
            self.router_log.append((req_id, "rejected"))
            return {"tier": "rejected", "task": task, "status": "reject",
                    "reason": "所有阶均无法处理"}

    def report(self) -> dict:
        route_counts = {}
        for _, route in self.router_log:
            route_counts[route] = route_counts.get(route, 0) + 1
        return {
            "total": len(self.router_log),
            "routes": route_counts,
            "micro_handled": self.micro.handled,
            "edge_handled": self.edge.handled,
            "cloud_handled": self.cloud.handled,
            "reject_count": self.reject_count,
        }


def run_hybrid_deployment_test(router: HybridDeploymentRouter,
                                num_requests: int = 30) -> list[dict]:
    results = []
    task_pool = [
        ("温度读取", "temp"), ("开关控制", "toggle"),
        ("状态查询", "status"), ("复杂分析", "analysis"),
        ("报表生成", "report"),
    ]
    for i in range(num_requests):
        # 第 15 个请求后断网
        if i == 15:
            router.cloud.toggle_network(False)
        task, prompt = task_pool[i % 5]
        result = router.route(task, prompt)
        results.append({"req_id": i, **result})
    return results


if __name__ == "__main__":
    router = HybridDeploymentRouter()
    print("=" * 56)
    print("混合部署调度 — 微端→边缘→云端 分流")
    print("=" * 56)
    results = run_hybrid_deployment_test(router, 30)

    for r in results:
        print(f"  req#{r['req_id']:>2d} | {r.get('task', '-'):>6s} | "
              f"tier={r.get('tier', '-'):>8s} | "
              f"status={r['status']:>14s} | "
              f"latency={r.get('latency_ms', '-')}")

    report = router.report()
    print(f"\n  分流报告: total={report['total']}")
    for route, count in report['routes'].items():
        print(f"    {route}: {count}")
    print(f"  各阶处理量: micro={report['micro_handled']} "
          f"edge={report['edge_handled']} cloud={report['cloud_handled']}")
    print(f"  拒答次数: {report['reject_count']}")
