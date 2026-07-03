# sliding_window
# 运行: python sliding_window.py

from collections import deque

class SlidingWindow:
    """滑动窗口工作记忆"""
    def __init__(self, max_messages=20, system_prompt=None):
        self.max_messages = max_messages
        self.system = system_prompt or ""
        self.buffer = deque(maxlen=max_messages)

    def add(self, role, content):
        self.buffer.append({"role": role, "content": content})

    def get_context(self):
        return [{"role": "system", "content": self.system}] + list(self.buffer)

    def info_loss_report(self, full_history):
        dropped = len(full_history) - len(self.buffer)
        roles = {}
        for m in full_history[:dropped]:
            roles[m["role"]] = roles.get(m["role"], 0) + 1
        return {"kept": len(self.buffer), "dropped": dropped,
                "dropped_by_role": roles}

if __name__ == "__main__":
    sw = SlidingWindow(max_messages=3, system_prompt="你是助手")
    history = [{"role":"user","content":f"问题{i}"} for i in range(6)]
    for m in history:
        sw.add(m["role"], m["content"])
    print(f"窗口内消息: {[m['content'] for m in sw.buffer]}")
    print(f"丢失报告: {sw.info_loss_report(history)}")

