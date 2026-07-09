"""
第5章源码：资源隔离——进程隔离+配额隔离+熔断隔离
模拟多 Agent 隔离场景：一个 Agent 出问题不影响其他
"""

import time
import random


class AgentSandbox:
    """Agent 沙箱——含资源限额"""

    def __init__(self, agent_id: str, cpu_limit: float, mem_limit_mb: float,
                 api_limit: int):
        self.agent_id = agent_id
        self.cpu_limit = cpu_limit
        self.mem_limit_mb = mem_limit_mb
        self.api_limit = api_limit
        self.cpu_used = 0.0
        self.mem_used = 0.0
        self.api_used = 0
        self.error_count = 0
        self.total_requests = 0
        self.melted = False

    def process(self, request: dict) -> dict:
        self.total_requests += 1
        if self.melted:
            return {"status": "melted", "agent": self.agent_id}

        cpu_needed = request.get("cpu", 0.1)
        mem_needed = request.get("mem_mb", 10)
        api_needed = request.get("api_calls", 1)

        # 检查配额
        if self.cpu_used + cpu_needed > self.cpu_limit:
            return {"status": "cpu_quota_exceeded", "agent": self.agent_id}
        if self.mem_used + mem_needed > self.mem_limit_mb:
            return {"status": "mem_quota_exceeded", "agent": self.agent_id}
        if self.api_used + api_needed > self.api_limit:
            return {"status": "api_quota_exceeded", "agent": self.agent_id}

        # 模拟执行
        self.cpu_used += cpu_needed
        self.mem_used += mem_needed
        self.api_used += api_needed
        time.sleep(cpu_needed * 0.01)

        # 模拟泄漏 Agent（memory leak scenario）
        if request.get("leak", False):
            self.mem_used += mem_needed * 2

        return {"status": "ok", "agent": self.agent_id,
                "cpu": cpu_needed, "mem_mb": mem_needed}

    def check_melt(self, error_threshold: float = 0.3, mem_threshold: float = 0.9):
        """熔断检查"""
        if self.total_requests > 0:
            error_rate = self.error_count / self.total_requests
            mem_usage = self.mem_used / self.mem_limit_mb
            if error_rate > error_threshold or mem_usage > mem_threshold:
                self.melted = True


class IsolatedPool:
    """隔离池——管理多个 Agent 沙箱"""

    def __init__(self):
        self.sandboxes: dict[str, AgentSandbox] = {}

    def add_sandbox(self, sandbox: AgentSandbox):
        self.sandboxes[sandbox.agent_id] = sandbox

    def process(self, agent_id: str, request: dict) -> dict:
        sandbox = self.sandboxes.get(agent_id)
        if not sandbox:
            return {"status": "agent_not_found"}
        result = sandbox.process(request)
        if result["status"] != "ok":
            sandbox.error_count += 1
        sandbox.check_melt()
        return result

    def health_report(self) -> dict:
        """全局健康报告"""
        report = {}
        for aid, sb in self.sandboxes.items():
            mem_pct = sb.mem_used / sb.mem_limit_mb if sb.mem_limit_mb > 0 else 0
            cpu_pct = sb.cpu_used / sb.cpu_limit if sb.cpu_limit > 0 else 0
            report[aid] = {
                "melted": sb.melted,
                "mem_usage_pct": round(mem_pct * 100, 1),
                "cpu_usage_pct": round(cpu_pct * 100, 1),
                "api_used": sb.api_used,
                "errors": sb.error_count,
                "ok_requests": sb.total_requests - sb.error_count,
            }
        return report


def run_isolation_test(pool: IsolatedPool, num_rounds: int = 10) -> list[dict]:
    results = []
    agents = list(pool.sandboxes.keys())
    for _ in range(num_rounds):
        for aid in agents:
            req = {
                "cpu": 0.2 + random.random() * 0.3,
                "mem_mb": 20 + random.random() * 30,
                "api_calls": 1,
                "leak": aid == "agent-leaky",
            }
            resp = pool.process(aid, req)
            results.append({"agent": aid, **resp})
    return results


if __name__ == "__main__":
    pool = IsolatedPool()
    pool.add_sandbox(AgentSandbox("agent-normal", cpu_limit=2.0, mem_limit_mb=200,
                                  api_limit=20))
    pool.add_sandbox(AgentSandbox("agent-leaky", cpu_limit=2.0, mem_limit_mb=200,
                                  api_limit=20))
    pool.add_sandbox(AgentSandbox("agent-minimal", cpu_limit=1.0, mem_limit_mb=100,
                                  api_limit=10))

    print("=" * 56)
    print("资源隔离 — Agent 隔离测试")
    print("=" * 56)
    results = run_isolation_test(pool, 15)

    for r in results:
        print(f"  {r['agent']:>15s} | {r['status']:>20s}")

    report = pool.health_report()
    print("\n  最终健康报告:")
    for aid, metrics in report.items():
        print(f"    {aid:>15s}: melted={metrics['melted']} | "
              f"mem={metrics['mem_usage_pct']:>5.1f}% | "
              f"cpu={metrics['cpu_usage_pct']:>5.1f}% | "
              f"errors={metrics['errors']}")
