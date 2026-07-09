"""
第6章源码：混合系统调度器——按任务类型判别分流三态
模拟三种任务类型分别路由到三态架构
"""

import time
import random
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    CRITICAL = "critical"


@dataclass
class ServiceTask:
    task_id: int
    task_type: TaskType
    prompt: str
    priority: int  # 1-5
    estimated_cpu: float
    tenant_id: str | None = None  # 多租户标识


class SimpleHandler:
    """单实例态处理器——简单无状态请求"""
    handled = 0

    def handle(self, task: ServiceTask) -> dict:
        self.handled += 1
        time.sleep(0.01)
        return {
            "handler": "simple", "task_id": task.task_id,
            "latency_s": 0.01, "status": "ok"
        }


class PoolHandler:
    """服务池态处理器——中等复杂请求"""
    handled = 0

    def handle(self, task: ServiceTask) -> dict:
        self.handled += 1
        latency = 0.03 + random.random() * 0.05
        time.sleep(latency * 0.1)
        # 模拟资源争用
        if task.estimated_cpu > 0.5 and random.random() < 0.15:
            return {
                "handler": "pool", "task_id": task.task_id,
                "latency_s": round(latency, 3), "status": "pool_contention"
            }
        return {
            "handler": "pool", "task_id": task.task_id,
            "latency_s": round(latency, 3), "status": "ok"
        }


class SchedulerHandler:
    """调度系统态处理器——高优先级/多租户请求"""
    handled = 0

    def handle(self, task: ServiceTask) -> dict:
        self.handled += 1
        latency = 0.05 + random.random() * 0.1
        time.sleep(latency * 0.1)
        return {
            "handler": "scheduler", "task_id": task.task_id,
            "latency_s": round(latency, 3), "status": "ok",
            "tenant": task.tenant_id,
            "priority": task.priority,
        }


class HybridDispatcher:
    """混合系统调度器"""

    def __init__(self):
        self.simple_handler = SimpleHandler()
        self.pool_handler = PoolHandler()
        self.scheduler_handler = SchedulerHandler()
        self.router_log: list[tuple[int, str]] = []

    def dispatch(self, task: ServiceTask) -> dict:
        """判别并分流"""
        if task.task_type == TaskType.SIMPLE:
            self.router_log.append((task.task_id, "simple"))
            return self.simple_handler.handle(task)
        elif task.task_type == TaskType.MODERATE:
            self.router_log.append((task.task_id, "pool"))
            return self.pool_handler.handle(task)
        else:  # CRITICAL
            self.router_log.append((task.task_id, "scheduler"))
            return self.scheduler_handler.handle(task)

    def report(self) -> dict:
        total = len(self.router_log)
        route_counts = {}
        for _, route in self.router_log:
            route_counts[route] = route_counts.get(route, 0) + 1
        return {
            "total": total,
            "routes": route_counts,
            "simple_handled": self.simple_handler.handled,
            "pool_handled": self.pool_handler.handled,
            "scheduler_handled": self.scheduler_handler.handled,
        }


def generate_task_pool(num_tasks: int) -> list[ServiceTask]:
    tasks = []
    for i in range(num_tasks):
        if i < 5:
            ttype = TaskType.CRITICAL
            pri = 5
            tenant = "enterprise"
        elif i < 15:
            ttype = TaskType.MODERATE
            pri = 3
            tenant = None
        else:
            ttype = TaskType.SIMPLE
            pri = 1
            tenant = None

        tasks.append(ServiceTask(
            task_id=i,
            task_type=ttype,
            prompt=f"task-{i}",
            priority=pri,
            estimated_cpu=0.1 + random.random() * 0.5,
            tenant_id=tenant,
        ))
    return tasks


def run_hybrid_test(dispatcher: HybridDispatcher, tasks: list[ServiceTask]) -> list[dict]:
    results = []
    for task in tasks:
        result = dispatcher.dispatch(task)
        results.append(result)
    return results


if __name__ == "__main__":
    dispatcher = HybridDispatcher()
    tasks = generate_task_pool(30)
    print("=" * 56)
    print("混合系统调度器 — 按任务类型分流三态")
    print("=" * 56)
    results = run_hybrid_test(dispatcher, tasks)

    for r in results:
        print(f"  task#{r['task_id']:>2d} | {r['handler']:>10s} | "
              f"{r['status']:>18s} | latency={r.get('latency_s', '-')}s")

    report = dispatcher.report()
    print(f"\n  分流报告: total={report['total']}")
    for route, count in report['routes'].items():
        print(f"    {route}: {count}")
    print(f"  各态处理量: simple={report['simple_handled']} "
          f"pool={report['pool_handled']} "
          f"scheduler={report['scheduler_handled']}")
