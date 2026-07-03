# async_batch_writer
# 运行: python async_batch_writer.py

import threading, queue

class AsyncBatchWriter:
    """异步批量写入器"""
    def __init__(self, store, batch_size=50, flush_interval=2.0):
        self.store, self.batch_size, self.flush_interval = store, batch_size, flush_interval
        self.queue = queue.Queue()
        self._running, self._thread = False, None
        self._stats = {"queued": 0, "written": 0, "dropped": 0}

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread: self._thread.join(timeout=5)
        self._flush()

    def write(self, content, metadata=None):
        try:
            self.queue.put_nowait({"content": content, "metadata": metadata})
            self._stats["queued"] += 1
            return {"status": "queued"}
        except queue.Full:
            self._stats["dropped"] += 1
            return {"status": "dropped"}

    def _flush_loop(self):
        while self._running:
            time.sleep(self.flush_interval)
            self._flush()

    def _flush(self):
        batch = []
        while len(batch) < self.batch_size:
            try: batch.append(self.queue.get_nowait())
            except queue.Empty: break
        for item in batch:
            self.store.add(item["content"], item["metadata"])
            self._stats["written"] += 1

    def stats(self):
        return dict(self._stats)


class TieredStorage:
    """分级存储: 热存/温存/冷存"""
    def __init__(self, hot_store, warm_store, cold_store):
        self.hot, self.warm, self.cold = hot_store, warm_store, cold_store

    def write(self, content, metadata=None):
        importance = (metadata or {}).get("importance", 0.3)
        if importance > 0.7: self.hot.write(content, metadata)
        elif importance > 0.4: self.warm.write(content, metadata)
        else: self.cold.write(content, metadata)

    def migrate(self):
        now = time.time()
        for item in self.hot.list_old(7):
            self.warm.write(item["content"], item["metadata"])
            self.hot.delete(item["id"])
        for item in self.warm.list_old(90):
            self.cold.write(item["content"], item["metadata"])
            self.warm.delete(item["id"])

if __name__ == "__main__":
    class MockStore:
        def __init__(self): self.items=[]
        def add(self,c,m): self.items.append(c)
    s = MockStore()
    aw = AsyncBatchWriter(s, batch_size=5, flush_interval=0.5)
    aw.start()
    import time as _t
    for i in range(12):
        aw.write(f"记忆_{i}", {"importance":0.5})
    _t.sleep(1.5)
    aw.stop()
    print(f"统计: {aw.stats()}")
    print(f"库大小: {len(s.items)}")
    # 确保 daemon 线程干净退出
    import sys; sys.stdout.flush()

