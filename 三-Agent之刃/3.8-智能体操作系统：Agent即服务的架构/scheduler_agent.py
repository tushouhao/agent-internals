"""
第4章源码：调度系统态——优先级队列与资源配额管理
模拟多级优先级队列+配额监控+抢占式调度
"""

import time
import random
from dataclasses import dataclass
from enum import IntEnum


class Priority(IntEnum):
    HIGH = 0
    NORMAL = 1
    LOW = 2


@dataclass
class ResourceQuota:
    """资源配额"""
    cpu_time_limit: float  # 秒
    api_call_limit: int
    memory_limit_mb: float


@dataclass
class AgentTask:
    """Agent 任务"""
    task_id: int
    priority: Priority
    prompt: str
    estimated_cpu: float
    api_calls: int
    submitted_at: float


class ResourceMonitor:
    """资源监控器"""

    def __init__(self):
        self.cpu_used = 0.0
        self.api_calls = 0
        self.memory_used = 0.0

    def check_quota(self, task: AgentTask, quota: ResourceQuota) -> bool:
        """检查任务是否超出配额"""
        if self.cpu_used + task.estimated_cpu > quota.cpu_time_limit:
            return False
        if self.api_calls + task.api_calls > quota.api_call_limit:
            return False
        return True

    def allocate(self, task: AgentTask):
        self.cpu_used += task.estimated_cpu
        self.api_calls += task.api_calls

    def release(self, task: AgentTask):
        self.cpu_used = max(0, self.cpu_used - task.estimated_cpu)
        self.api_calls = max(0, self.api_calls - task.api_calls)


class PriorityScheduler:
    """优先级调度器——三级优先级队列+抢占+公平调度"""

    def __init__(self):
        self.queues: dict[Priority, list[AgentTask]] = {
            Priority.HIGH: [],
            Priority.NORMAL: [],
            Priority.LOW: [],
        }
        self.monitor = ResourceMonitor()
        self.quota = ResourceQuota(
            cpu_time_limit=10.0,
            api_call_limit=50,
            memory_limit_mb=1024,
        )
        self.current_task: AgentTask | None = None
        self.completed = []
        self.preempted = []
        self.starved = []
        self.fairness_counter = {Priority.HIGH: 0, Priority.NORMAL: 0, Priority.LOW: 0}
        self.time_slice = 0.5  # 时间片

    def submit(self, task: AgentTask):
        self.queues[task.priority].append(task)

    def _pick_next(self) -> AgentTask | None:
        """选择下一个执行的任务——优先级+防饿死"""
        now = time.time()

        # 检查三个队列
        for pri in [Priority.HIGH, Priority.NORMAL, Priority.LOW]:
            if self.queues[pri]:
                task = self.queues[pri][0]
                # 公平调度：低优等待超 5s 提升优先级
                if pri == Priority.LOW and (now - task.submitted_at) > 5.0:
                    self.queues[pri].pop(0)
                    task.priority = Priority.NORMAL
                    self.queues[Priority.NORMAL].append(task)
                    self.starved.append(task.task_id)
                    continue
                return self.queues[pri].pop(0)

        return None

    def schedule(self) -> dict:
        """执行一次调度"""
        # 抢占检查
        if self.current_task:
            high_pri_tasks = bool(self.queues[Priority.HIGH])
            if high_pri_tasks and self.current_task.priority != Priority.HIGH:
                # 挂起当前任务
                self.preempted.append(self.current_task.task_id)
                self.current_task.priority = Priority(min(
                    self.current_task.priority.value + 1, 2))
                self.queues[self.current_task.priority].append(self.current_task)
                self.current_task = None

        if not self.current_task:
            task = self._pick_next()
            if not task:
                return {"status": "idle"}
            if not self.monitor.check_quota(task, self.quota):
                return {"status": "quota_exceeded", "task_id": task.task_id}
            self.current_task = task
            self.monitor.allocate(task)
            self.fairness_counter[task.priority] += 1

        # 模拟执行（时间片内）
        exec_time = min(self.time_slice, self.current_task.estimated_cpu)
        time.sleep(exec_time * 0.01)
        self.current_task.estimated_cpu -= exec_time

        if self.current_task.estimated_cpu <= 0:
            self.completed.append(self.current_task.task_id)
            self.monitor.release(self.current_task)
            self.current_task = None

        return {
            "status": "running",
            "current_task_id": self.current_task.task_id if self.current_task else None,
            "queue_sizes": {p.name: len(q) for p, q in self.queues.items()},
            "fairness": dict(self.fairness_counter),
        }


def run_scheduler_test(scheduler: PriorityScheduler, num_tasks: int = 20) -> list[dict]:
    logs = []
    for i in range(num_tasks):
        pri = Priority.HIGH if i < 3 else (
            Priority.NORMAL if i < 10 else Priority.LOW)
        task = AgentTask(
            task_id=i,
            priority=pri,
            prompt=f"task-{i}",
            estimated_cpu=0.3 + random.random() * 0.5,
            api_calls=random.randint(1, 3),
            submitted_at=time.time(),
        )
        scheduler.submit(task)

    for _ in range(30):
        result = scheduler.schedule()
        logs.append(result)
        if result["status"] == "idle" and all(not q for q in scheduler.queues.values()):
            break
    return logs


if __name__ == "__main__":
    scheduler = PriorityScheduler()
    print("=" * 56)
    print("调度系统态 — 优先级调度与资源配额")
    print("=" * 56)
    logs = run_scheduler_test(scheduler, 20)
    for i, log in enumerate(logs):
        if log["status"] == "idle":
            continue
        qs = log.get("queue_sizes", {})
        print(f"  step#{i:>2d} | {log['status']:>15s} | "
              f"current={log.get('current_task_id', '-')} | "
              f"queues={qs}")

    print(f"\n  完成: {scheduler.completed}")
    print(f"  抢占: {scheduler.preempted}")
    print(f"  饥饿提升: {scheduler.starved}")
    print(f"  公平计数: {dict(scheduler.fairness_counter)}")
