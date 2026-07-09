"""
第6章源码：能耗预算管理——电池设备的 Agent 续航
模拟推理能耗 + 睡眠调度 + 能耗预算三策略
"""

import random


class PowerProfile:
    """功耗画像——各状态能耗"""

    def __init__(self):
        self.inference_power_mw = 500  # 推理 500mW
        self.idle_power_mw = 50        # 闲置 50mW
        self.sleep_power_mw = 5        # 深度睡眠 5mW
        self.sampling_power_mw = 100   # 采样 100mW


class EnergyBudgetManager:
    """能耗预算管理器"""

    def __init__(self, battery_capacity_mwh: float = 1000):
        self.battery_mwh = battery_capacity_mwh
        self.remaining_mwh = battery_capacity_mwh
        self.power = PowerProfile()
        self.inference_count = 0
        self.skip_count = 0
        self.sleep_count = 0
        self.degraded_count = 0
        self.tasks_total = 0
        self.tasks_completed = 0

    def inference_energy(self, latency_ms: float) -> float:
        """单次推理能耗（mWh）"""
        hours = latency_ms / 1000 / 3600
        return self.power.inference_power_mw * hours

    def sleep_energy(self, sleep_ms: float) -> float:
        hours = sleep_ms / 1000 / 3600
        return self.power.sleep_power_mw * hours

    def can_infer(self, estimated_latency_ms: float = 50) -> bool:
        needed = self.inference_energy(estimated_latency_ms)
        # 临界保护：剩余低于 10% 仅保核心
        if self.remaining_mwh < self.battery_mwh * 0.1:
            return False
        return self.remaining_mwh >= needed

    def consume(self, energy_mwh: float):
        self.remaining_mwh = max(0, self.remaining_mwh - energy_mwh)

    def battery_pct(self) -> float:
        return self.remaining_mwh / self.battery_mwh * 100


class EnergyAwareAgent:
    """能耗感知 Agent——推理控制 + 睡眠调度 + 预算管理"""

    def __init__(self, battery_mwh: float = 1000):
        self.budget = EnergyBudgetManager(battery_mwh)
        self.confidence_threshold = 0.7  # 置信跳过阈值

    def process(self, task: str, confidence: float, estimated_latency_ms: float = 50) -> dict:
        self.budget.tasks_total += 1
        # 策略一：高置信跳过推理
        if confidence >= self.confidence_threshold:
            self.budget.skip_count += 1
            return {"status": "skipped", "reason": "高置信跳过", "task": task}

        # 策略三：能耗预算检查
        if not self.budget.can_infer(estimated_latency_ms):
            self.budget.degraded_count += 1
            return {"status": "budget_low", "reason": "能耗预算不足降频", "task": task}

        # 策略一：执行推理
        energy = self.budget.inference_energy(estimated_latency_ms)
        self.budget.consume(energy)
        self.budget.inference_count += 1
        self.budget.tasks_completed += 1
        return {
            "status": "ok", "task": task,
            "energy_mwh": round(energy, 6),
            "battery_pct": round(self.budget.battery_pct(), 1),
        }

    def sleep(self, sleep_ms: float = 1000) -> dict:
        energy = self.budget.sleep_energy(sleep_ms)
        self.budget.consume(energy)
        self.budget.sleep_count += 1
        return {"sleep_ms": sleep_ms, "energy_mwh": round(energy, 6),
                "battery_pct": round(self.budget.battery_pct(), 1)}


def run_energy_test(agent: EnergyAwareAgent, num_cycles: int = 20) -> list[dict]:
    results = []
    tasks = ["温度读取", "开关控制", "状态查询", "复杂分析", "报表生成"]
    for i in range(num_cycles):
        task = tasks[i % 5]
        confidence = random.random()
        result = agent.process(task, confidence, estimated_latency_ms=50)
        result["cycle"] = i
        results.append(result)
        # 无任务时睡眠
        if i % 3 == 0:
            sleep_result = agent.sleep(sleep_ms=500)
            results.append({"cycle": i, "type": "sleep", **sleep_result})
    return results


if __name__ == "__main__":
    agent = EnergyAwareAgent(battery_mwh=500)  # 小电池假设
    print("=" * 56)
    print("能耗预算管理 — 电池设备 Agent 续航")
    print("=" * 56)
    results = run_energy_test(agent, 30)

    for r in results:
        if r.get("type") == "sleep":
            print(f"  cycle#{r['cycle']:>2d} | SLEEP | "
                  f"energy={r['energy_mwh']:.6f} | battery={r['battery_pct']:.1f}%")
        else:
            print(f"  cycle#{r['cycle']:>2d} | {r['status']:>10s} | "
                  f"task={r.get('task', '-'):>6s} | "
                  f"battery={r.get('battery_pct', '-')}%")

    print(f"\n  任务总计: {agent.budget.tasks_total}")
    print(f"  推理完成: {agent.budget.inference_count}")
    print(f"  高置信跳过: {agent.budget.skip_count}")
    print(f"  预算降频: {agent.budget.degraded_count}")
    print(f"  睡眠次数: {agent.budget.sleep_count}")
    print(f"  剩余电量: {agent.budget.battery_pct():.1f}%")
