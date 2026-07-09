# 4.8 协作失控：消息错序与协同失序 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.8
> 正文：`四-Agent之盾/4.8-协作失控：消息错序与协同失序/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `message_disorder.py` | 消息顺序错乱，错序率 100% | 第 1 章 消息错序阶 |
| 2 | `coordination_disorder.py` | 协同失序检测，漏检率 13% | 第 2 章 协同失序阶 |
| 3 | `collaboration_mismatch.py` | 跨要求适配检测，失配率 100% | 第 3 章 协作失配阶 |
| 4 | `hybrid_collab_router.py` | 按协作深度判别分流三级 + 拚答护栏 | 第 4 章 混合路由器 |
| 5 | `disorder_fallback.py` | 失序漏检降级兜底三策略，残留率降到 2% | 第 5 章 降级兜底 |
| 6 | `disorder_detect_medium.py` | 失序检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `collab_residual.py` | 协作残留率量化——失序检测 2% vs 消息错序 100% 核心 KPI | 第 7 章 协作残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.8-协作失控：消息错序与协同失序
python message_disorder.py
python coordination_disorder.py
python collaboration_mismatch.py
python hybrid_collab_router.py
python disorder_fallback.py
python disorder_detect_medium.py
python collab_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
