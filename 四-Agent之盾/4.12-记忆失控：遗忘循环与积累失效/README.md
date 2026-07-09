# 4.12 记忆失控：遗忘循环与积累失效 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.12
> 正文：`四-Agent之盾/4.12-记忆失控：遗忘循环与积累失效/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `forget_loop.py` | 记忆无积累，遗忘率 100% | 第 1 章 遗忘循环阶 |
| 2 | `accumulate_failure.py` | 积累失效检测，漏检率 17% | 第 2 章 积累失效阶 |
| 3 | `memory_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 记忆失配阶 |
| 4 | `hybrid_memory_router.py` | 按记忆深度判别分流三级 + 拚答护栏 | 第 4 章 混合路由器 |
| 5 | `failure_fallback.py` | 效降级兜底三策略，残留率降到 2% | 第 5 章 降级兜底 |
| 6 | `failure_detect_medium.py` | 效检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `memory_residual.py` | 记忆残留率量化——失效检测 2% vs 遗忘循环 100% 核心 KPI | 第 7 章 记忆残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.12-记忆失控：遗忘循环与积累失效
python forget_loop.py
python accumulate_failure.py
python memory_mismatch.py
python hybrid_memory_router.py
python failure_fallback.py
python failure_detect_medium.py
python memory_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
