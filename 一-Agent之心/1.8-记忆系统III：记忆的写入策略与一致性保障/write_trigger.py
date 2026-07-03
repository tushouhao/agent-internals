# write_trigger
# 运行: python write_trigger.py

import time

class WriteTrigger:
    """写入时机触发器"""
    def __init__(self, strategy="event", store=None):
        self.strategy, self.store = strategy, store
        self.batch_buffer, self.batch_size = [], 20
        self.event_keywords = {"错误", "完成", "决策", "用户偏好", "确认"}

    def consider_write(self, message, step_info):
        """根据策略决定是否写入"""
        if self.strategy == "every_turn":
            return self._write_now(message, step_info)
        elif self.strategy == "event":
            if self._is_event(message, step_info):
                return self._write_now(message, step_info)
            return {"written": False, "reason": "non_event"}
        elif self.strategy == "batch":
            return self._buffer_write(message, step_info)
        return {"written": False, "reason": "unknown_strategy"}

    def _is_event(self, message, step_info=None):
        content = message.get("content", "")
        if any(kw in content for kw in self.event_keywords):
            return True
        if message.get("role") == "tool" and "error" in content.lower():
            return True
        if step_info and step_info.get("is_decision_point"):
            return True
        return False

    def _write_now(self, message, step_info):
        mid = self.store.add(message["content"], {
            "role": message["role"],
            "step": step_info.get("step", 0) if step_info else 0,
            "timestamp": time.time()})
        return {"written": True, "id": mid, "strategy": self.strategy}

    def _buffer_write(self, message, step_info):
        self.batch_buffer.append((message, step_info))
        if len(self.batch_buffer) >= self.batch_size:
            return self._flush_buffer()
        return {"written": False, "buffered": len(self.batch_buffer)}

    def _flush_buffer(self):
        written = 0
        for msg, info in self.batch_buffer:
            self.store.add(msg["content"], {"role": msg["role"],
                "step": info.get("step", 0) if info else 0})
            written += 1
        self.batch_buffer = []
        return {"written": written, "strategy": "batch_flush"}

if __name__ == "__main__":
    class MockStore:
        def __init__(self): self.items=[]
        def add(self,c,m): self.items.append((c,m)); return len(self.items)-1
    s = MockStore()
    for strat in ["every_turn","event","batch"]:
        wt = WriteTrigger(strat, s)
        for i in range(5):
            msg = {"role":"user","content":f"消息{i}" + ("完成" if i==3 else "")}
            r = wt.consider_write(msg, {"step":i,"is_decision_point":i==2})
            print(f"  [{strat}] 步{i}: {r}")
        if strat == "batch":
            print(f"  批量刷新: {wt._flush_buffer()}")
        print(f"  库大小: {len(s.items)}")

