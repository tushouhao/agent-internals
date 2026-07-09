# 4.13 反思失控：自省失效与元认知缺失 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.13
> 正文：`四-Agent之盾/4.13-反思失控：自省失效与元认知缺失/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `introspect_failure.py` | 无自省，失省率 100% | 第 1 章 自省失效阶 |
| 2 | `metacog_missing.py` | 元认知缺失检测，漏检率 18% | 第 2 章 元认知缺失阶 |
| 3 | `reflect_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 反思失配阶 |
| 4 | `hybrid_reflect_router.py` | 按反思深度判别分流三级 + 拚答护栏 | 第 4 章 混合路由器 |
| 5 | `miss_fallback.py` | 漏识降级兜底三策略，残留率降到 3% | 第 5 章 降级兜底 |
| 6 | `miss_detect_medium.py` | 漏识检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `reflect_residual.py` | 反思残留率量化——漏识检测 3% vs 自省失效 100% 核心 KPI | 第 7 章 反思残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.13-反思失控：自省失效与元认知缺失
python introspect_failure.py
python metacog_missing.py
python reflect_mismatch.py
python hybrid_reflect_router.py
python miss_fallback.py
python miss_detect_medium.py
python reflect_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
