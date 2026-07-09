# 4.9 可观测失控：盲飞运行与诊断缺失 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.9
> 正文：`四-Agent之盾/4.9-可观测失控：盲飞运行与诊断缺失/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `blind_flying.py` | 无可观测信号，盲飞率 100% | 第 1 章 盲飞运行阶 |
| 2 | `diagnosis_missing.py` | 诊断缺失检测，漏检率 14% | 第 2 章 诊断缺失阶 |
| 3 | `observable_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 可观测失配阶 |
| 4 | `hybrid_obs_router.py` | 按可观测深度判别分流三级 + 拚答护栏 | 第 4 章 混合路由器 |
| 5 | `diagnosis_fallback.py` | 漏诊降级兜底三策略，残留率降到 2% | 第 5 章 降级兜底 |
| 6 | `diagnosis_detect_medium.py` | 诊断检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `observable_residual.py` | 可观测残留率量化——诊断检测 2% vs 盲飞运行 100% 核心 KPI | 第 7 章 可观测残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.9-可观测失控：盲飞运行与诊断缺失
python blind_flying.py
python diagnosis_missing.py
python observable_mismatch.py
python hybrid_obs_router.py
python diagnosis_fallback.py
python diagnosis_detect_medium.py
python observable_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
