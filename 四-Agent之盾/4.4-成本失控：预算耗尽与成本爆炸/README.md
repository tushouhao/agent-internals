# 4.4 成本失控：预算耗尽与成本爆炸 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.4
> 正文：`四-Agent之盾/4.4-成本失控：预算耗尽与成本爆炸/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `budget_exhaust.py` | 多轮累积成本耗尽预算，拒答率 100% | 第 1 章 预算耗尽阶 |
| 2 | `cost_explosion.py` | 单轮突增检测，漏检率 14% | 第 2 章 成本爆炸阶 |
| 3 | `cost_mismatch.py` | 跨预算适配检测，失配率 100% | 第 3 章 成本失配阶 |
| 4 | `hybrid_cost_router.py` | 按成本深度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `spike_fallback.py` | 突增漏检降级兜底三策略，残留率降到 4% | 第 5 章 降级兜底 |
| 6 | `spike_detect_medium.py` | 突增检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `cost_residual.py` | 成本残留率量化——突增检测 4% vs 预算耗尽 100% 核心 KPI | 第 7 章 成本残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.4-成本失控：预算耗尽与成本爆炸
python budget_exhaust.py
python cost_explosion.py
python cost_mismatch.py
python hybrid_cost_router.py
python spike_fallback.py
python spike_detect_medium.py
python cost_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
