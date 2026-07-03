# cycle_detector
# 运行: python cycle_detector.py

import time, hashlib

class CycleDetector:
    """子目标环检测器"""
    def __init__(self, window_size=10):
        self.history = []           # 子目标执行记录
        self.window = window_size   # 检测窗口

    def record(self, subgoal_name, result_hash):
        """记录子目标执行"""
        self.history.append({
            "name": subgoal_name,
            "hash": result_hash,
            "timestamp": time.time()
        })
        return self.detect()

    def detect(self):
        """检测是否存在子目标环"""
        recent = self.history[-self.window:]

        # 1. 相同子目标连续出现检查
        if len(recent) >= 3:
            last_three = [r["name"] for r in recent[-3:]]
            if len(set(last_three)) == 1:
                return {"type": "self_loop", "subgoal": last_three[0]}

        # 2. 子目标序列周期检查（A-B-A-B 模式）
        if len(recent) >= 4:
            seq = [r["name"] for r in recent]
            for period in range(2, len(seq) // 2 + 1):
                pattern = seq[-period:]
                if seq[-2*period:-period] == pattern:
                    return {"type": "deadly_embrace", "pattern": pattern}

        # 3. 结果哈希重复检查（相同输入输出）
        if len(recent) >= 2:
            if recent[-1]["hash"] == recent[-2]["hash"]:
                return {"type": "result_stuck", "subgoal": recent[-1]["name"]}

        return None

if __name__ == "__main__":
    cd = CycleDetector(window_size=10)

    # 场景1: 自循环（同名连续3次）
    print("--- 场景1: 自循环 ---")
    cd1 = CycleDetector(window_size=10)
    for _ in range(3):
        r = cd1.record("retry_search", hashlib.md5(b"x").hexdigest())
    print(f"  检测: {r}")

    # 场景2: 死锁（A-B-A-B 周期）
    print("--- 场景2: 死锁周期 ---")
    cd2 = CycleDetector(window_size=10)
    for s in ["A", "B", "A", "B"]:
        cd2.record(s, hashlib.md5(s.encode()).hexdigest())
    print(f"  检测: {cd2.detect()}")

    # 场景3: 结果停滞
    print("--- 场景3: 结果停滞 ---")
    cd3 = CycleDetector(window_size=10)
    h = hashlib.md5(b"same").hexdigest()
    cd3.record("step1", h)
    cd3.record("step2", h)
    print(f"  检测: {cd3.detect()}")

    # 场景4: 正常无环
    print("--- 场景4: 正常 ---")
    cd4 = CycleDetector(window_size=10)
    for s in ["A", "B", "C"]:
        cd4.record(s, hashlib.md5(s.encode()).hexdigest())
    print(f"  检测: {cd4.detect()}")
