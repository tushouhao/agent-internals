# 1.8 写入之道：记忆的写入策略与一致性保障 — 源码

| 文件 | 说明 |
|---|---|
| `write_trigger.py` | 写入时机触发器（每轮/事件/批量） |
| `write_filter.py` | 写入内容三层过滤 |
| `versioned_store.py` | 向量版本控制记忆库（VDB） |
| `lock_memory.py` | 悲观锁与乐观锁 |
| `async_batch_writer.py` | 异步批量写入 + 分级存储 |
| `quality_monitor.py` | 写入质量监控与反馈 |

**GitHub**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
