# quality_monitor
# 运行: python quality_monitor.py

class WriteQualityMonitor:
    """写入质量监控器"""
    def __init__(self, store):
        self.store = store
        self.metrics = {"total_writes": 0, "later_retrieved": 0,
                        "never_retrieved": 0, "duplicate_writes": 0, "noise_writes": 0}

    def record_write(self, memory_id, content, metadata):
        self.metrics["total_writes"] += 1
        if self._is_likely_noise(content):
            self.metrics["noise_writes"] += 1

    def record_retrieval(self, memory_id):
        self.metrics["later_retrieved"] += 1

    def _is_likely_noise(self, content):
        return len(content) < 5 or (content.count(' ') == 0 and len(content) < 3)

    def report(self):
        total = self.metrics["total_writes"]
        if total == 0: return {"error": "no writes"}
        return {"total_writes": total,
                "retrieval_rate": self.metrics["later_retrieved"] / total,
                "dead_write_rate": self.metrics["never_retrieved"] / total,
                "noise_rate": self.metrics["noise_writes"] / total,
                "health_score": self._health_score()}

    def _health_score(self):
        if self.metrics["total_writes"] == 0: return 0
        retrieval = self.metrics["later_retrieved"] / self.metrics["total_writes"]
        noise = self.metrics["noise_writes"] / self.metrics["total_writes"]
        return max(0, int(100 * retrieval * (1 - noise)))

    def recommend(self):
        report = self.report()
        if report.get("noise_rate", 0) > 0.15:
            return {"action": "strengthen_filter", "reason": "噪声率高"}
        if report.get("dead_write_rate", 0) > 0.6:
            return {"action": "narrow_trigger", "reason": "死写率高, 收紧触发"}
        if report.get("retrieval_rate", 0) < 0.3:
            return {"action": "improve_annotation", "reason": "检索率低, 改进标注"}
        return {"action": "maintain", "reason": "指标健康"}

if __name__ == "__main__":
    m = WriteQualityMonitor(None)
    m.record_write(1,"订单 OD2024001 金额 12500",{})
    m.record_write(2,"好的",{})
    m.record_write(3,"用户偏好加急",{})
    m.record_retrieval(1)
    m.record_retrieval(3)
    print(f"报告: {m.report()}")
    print(f"建议: {m.recommend()}")

