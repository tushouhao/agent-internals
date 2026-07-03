# versioned_store
# 运行: python versioned_store.py
import time

class VersionedMemoryStore:
    """向量版本控制记忆库（VDB）"""
    def __init__(self):
        self.versions = {}

    def write(self, key, value, agent_id, base_version=None):
        """带版本号的写入"""
        current = self.versions.get(key, [])
        current_version = current[-1]["version"] if current else 0
        if base_version is not None and base_version != current_version:
            return {"status": "conflict", "current_version": current_version,
                    "your_base": base_version,
                    "resolution": self._auto_merge(current[-1]["value"], value) if current else value}
        new_version = current_version + 1
        current.append({"version": new_version, "value": value,
                        "agent_id": agent_id, "timestamp": time.time()})
        self.versions[key] = current
        return {"status": "ok", "version": new_version}

    def read(self, key, version=None):
        history = self.versions.get(key, [])
        if not history: return None
        if version is not None:
            return next((h for h in history if h["version"] == version), None)
        return history[-1]

    def _auto_merge(self, old_value, new_value):
        if isinstance(old_value, dict) and isinstance(new_value, dict):
            merged = old_value.copy()
            merged.update(new_value)
            return {"merged": True, "value": merged}
        return {"merged": False, "old": old_value, "new": new_value}

if __name__ == "__main__":
    vs = VersionedMemoryStore()
    r1 = vs.write("order_1","待发货","A1")
    print(f"A1 写入: {r1}")
    r2 = vs.write("order_1","已发货","A2",base_version=1)
    print(f"A2 正常写入: {r2}")
    r3 = vs.write("order_1","已取消","A3",base_version=1)
    print(f"A3 冲突: {r3}")
    print(f"历史: {vs.versions['order_1']}")

