# 4.6 质量失控：产物降级与质量退化 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.6
> 正文：`四-Agent之盾/4.6-质量失控：产物降级与质量退化/index.md`

## 文件清单

| # | 文件名 | 功能 | �章对应 |
|---|---|---|---|
| 1 | `artifact_degrade.py` | 低质量产物降级，降级率 100% | 第 1 章 产物降级阶 |
| 2 | `quality_decay.py` | 多轮退化检测，漏检率 12% | 第 2 章 质量退化阶 |
| 3 | `quality_mismatch.py` | �跨要求适配检测，失配率 100% | 第 3 章 质量失配阶 |
| 4 | `hybrid_quality_router.py` | 按质量深度判别分流三级 + 拠答护栏 | 第 4 章 混合路由器 |
| 5 | `decay_fallback.py` | 退化漏检降级兜底三策略，残留率降到 2% | 第 5 章 降级兜底 |
| 6 | `decay_detect_medium.py` | 退化检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `quality_residual.py` | 质量残留率量化——退化检测 2% vs 产物降级 100% 核心 KPI | 第 7 章 质量残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.6-质量失控：产物降级与质量退化
python artifact_degrade.py
python quality_decay.py
python quality_mismatch.py
python hybrid_quality_router.py
python decay_fallback.py
python decay_detect_medium.py
python quality_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
