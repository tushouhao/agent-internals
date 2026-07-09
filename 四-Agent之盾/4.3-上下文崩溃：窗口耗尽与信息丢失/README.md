# 4.3 上下文崩溃：窗口耗尽与信息丢失 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.3
> 正文：`四-Agent之盾/4.3-上下文崩溃：窗口耗尽与信息丢失/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `window_exhaust.py` | 多轮累积 token 耗尽窗口，拒答率 100% | 第 1 章 窗口耗尽阶 |
| 2 | `info_loss.py` | 长上下文关键检测，漏检率 12% | 第 2 章 信息丢失阶 |
| 3 | `truncation_recovery.py` | 超长截断兜底反推，崩救率 100% | 第 3 章 截断崩救阶 |
| 4 | `hybrid_ctx_router.py` | 按上下文深度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `key_fallback.py` | 关键漏检降级兜底三策略，残留率降到 4% | 第 5 章 降级兜底 |
| 6 | `key_detect_medium.py` | 关键检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `info_residual.py` | 信息残留率量化——关键检测 4% vs 窗口耗尽 100% 核心 KPI | 第 7 章 信息残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.3-上下文崩溃：窗口耗尽与信息丢失
python window_exhaust.py
python info_loss.py
python truncation_recovery.py
python hybrid_ctx_router.py
python key_fallback.py
python key_detect_medium.py
python info_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
