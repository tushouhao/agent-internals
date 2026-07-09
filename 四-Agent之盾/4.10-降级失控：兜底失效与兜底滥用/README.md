# 4.10 降级失控：兜底失效与兜底滥用 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.10
> 正文：`四-Agent之盾/4.10-降级失控：兜底失效与兜底滥用/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `fallback_failure.py` | 无降级兜底，失效率 100% | 第 1 章 兜底失效阶 |
| 2 | `fallback_abuse.py` | 兜底滥用检测，漏检率 15% | 第 2 章 兜底滥用阶 |
| 3 | `degrade_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 降级失配阶 |
| 4 | `hybrid_degrade_router.py` | 按降级深度判别分流三级 + 拚答护栏 | 第 4 章 混合路由器 |
| 5 | `abuse_fallback.py` | 滥用降级兜底三策略，残留率降到 2% | 第 5 章 降级兜底 |
| 6 | `abuse_detect_medium.py` | 滥用检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `degrade_residual.py` | 降级残留率量化——滥用检测 2% vs 兜底失效 100% 核心 KPI | 第 7 章 降级残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.10-降级失控：兜底失效与兜底滥用
python fallback_failure.py
python fallback_abuse.py
python degrade_mismatch.py
python hybrid_degrade_router.py
python abuse_fallback.py
python abuse_detect_medium.py
python degrade_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
