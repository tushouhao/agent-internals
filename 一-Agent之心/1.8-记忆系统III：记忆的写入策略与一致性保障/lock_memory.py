# lock_memory
# 运行: python lock_memory.py
import time

class PessimisticLockMemory:
    """悲观锁记忆库"""
    def __init__(self):
        self.store, self.locks = {}, {}
        self.lock_timeout = 30

    def acquire_lock(self, key, agent_id):
        existing = self.locks.get(key)
        if existing and existing.get("agent_id") != agent_id:
            if existing.get("timestamp", 0) + self.lock_timeout > time.time():
                return {"locked": False, "holder": existing["agent_id"]}
        self.locks[key] = {"agent_id": agent_id, "timestamp": time.time()}
        return {"locked": True}

    def write(self, key, value, agent_id):
        lock = self.acquire_lock(key, agent_id)
        if not lock["locked"]:
            return {"status": "blocked", "holder": lock["holder"]}
        self.store[key] = {"value": value, "writer": agent_id, "timestamp": time.time()}
        self.locks.pop(key, None)
        return {"status": "ok"}

    def read(self, key):
        return self.store.get(key)


class OptimisticLockMemory:
    """乐观锁记忆库（CAS 机制）"""
    def __init__(self):
        self.store = {}

    def read(self, key):
        entry = self.store.get(key)
        return {"value": entry["value"], "version": entry["version"]} if entry else {"value": None, "version": 0}

    def write(self, key, value, agent_id, expected_version):
        current = self.store.get(key)
        current_version = current["version"] if current else 0
        if expected_version != current_version:
            return {"status": "conflict", "current_version": current_version}
        self.store[key] = {"value": value, "version": current_version + 1, "writer": agent_id}
        return {"status": "ok", "version": current_version + 1}

if __name__ == "__main__":
    pm = PessimisticLockMemory()
    r1 = pm.write("k1","v1","A1")
    r2 = pm.write("k1","v2","A2")
    print(f"悲观锁 A1: {r1}, A2: {r2}")
    om = OptimisticLockMemory()
    r = om.write("k1","v1","A1",0)
    print(f"乐观锁 A1: {r}")
    r = om.write("k1","v2","A2",0)
    print(f"乐观锁 A2 冲突: {r}")
    r = om.write("k1","v2","A2",1)
    print(f"乐观锁 A2 重试: {r}")

