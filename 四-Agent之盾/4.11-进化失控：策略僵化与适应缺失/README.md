# 4.11 进化失控：策略僵化与适应缺失 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.11
> 正文：`四-Agent之盾/4.11-进化失控：策略僵化与适应缺失/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `strategy_rigid.py` | 策略无适应，僵化率 100% | 第 1 章 策略僵化阶 |
| 2 | `adaptation_missing.py` | 适应缺失检测，漏检率 16% | 第 2 章 适应缺失阶 |
| 3 | `evolve_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 进化失配阶 |
| 4 | `hybrid_evolve_router.py` | 按进化深度判别分流三级 + 拚答护栏 | 第 4 章 混合路由器 |
| 5 | `adaptation_fallback.py` | 漏适降级兜底三策略，残留率降到 2% | 第 5 章 降级兜底 |
| 6 | `adaptation_detect_medium.py` | 适应检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `evolve_residual.py` | 进化残留率量化——适应检测 2% vs 策略僵化 100% 核心 KPI | 第 7 章 进化残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.11-进化失控：策略僵化与适应缺失
python strategy_rigid.py
python adaptation_missing.py
python evolve_mismatch.py
python hybrid_evolve_router.py
python adaptation_fallback.py
python adaptation_detect_medium.py
python evolve_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
