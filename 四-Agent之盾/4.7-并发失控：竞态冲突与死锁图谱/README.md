# 4.7 并发失控：竞态冲突与死锁图谱 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.7
> 正文：`四-Agent之盾/4.7-并发失控：竞态冲突与死锁图谱/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `race_conflict.py` | 并发访问共享冲突，冲突率 100% | 第 1 章 竞态冲突阶 |
| 2 | `deadlock_graph.py` | 循环等待死锁检测，漏检率 14% | 第 2 章 死锁图谱阶 |
| 3 | `concurrency_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 并发失配阶 |
| 4 | `hybrid_concurrency_router.py` | 按并发深度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `deadlock_fallback.py` | 死锁漏检降级兜底三策略，残留率降到 4% | 第 5 章 降级兜底 |
| 6 | `deadlock_detect_medium.py` | 死锁检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `concurrency_residual.py` | 并发残留率量化——死锁检测 4% vs �竞态冲突 100% 核心 KPI | 第 7 章 并发残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.7-并发失控：竞态冲突与死锁图谱
python race_conflict.py
python deadlock_graph.py
python concurrency_mismatch.py
python hybrid_concurrency_router.py
python deadlock_fallback.py
python deadlock_detect_medium.py
python concurrency_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
