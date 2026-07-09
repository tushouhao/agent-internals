# 4.2 工具调用失败：参数幻觉与语义漂移 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.2
> 正文：`四-Agent之盾/4.2-工具调用失败：参数幻觉与语义漂移/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `param_hallucination.py` | LLM 生成参数幻觉，调用率 0% | 第 1 章 参数幻觉阶 |
| 2 | `semantic_drift.py` | 跨轮漂移检测，漏检率 4% | 第 2 章 语义漂移阶 |
| 3 | `tool_mismatch.py` | 跨版本签名校验，失配率 100% | 第 3 章 工具失配阶 |
| 4 | `hybrid_call_router.py` | 按调用深度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `drift_fallback.py` | 漂移漏检降级兜底三策略，残留率降到 1% | 第 5 章 降级兜底 |
| 6 | `drift_detect_medium.py` | 漂移检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `drift_residual.py` | 漂移残留率量化——漂移检测 4% vs 参数幻觉 100% 核心 KPI | 第 7 章 漂移残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.2-工具调用失败：参数幻觉与语义漂移
python param_hallucination.py
python semantic_drift.py
python tool_mismatch.py
python hybrid_call_router.py
python drift_fallback.py
python drift_detect_medium.py
python drift_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
