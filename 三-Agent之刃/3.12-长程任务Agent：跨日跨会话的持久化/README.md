# 3.12 长程任务 Agent：跨日跨会话的持久化 — 源码说明

> 专栏：《AI Agent 技术内幕》卷三 · Agent 之刃
> 篇号：3.12
> 正文：`三-Agent之刃/3.12-长程任务Agent：跨日跨会话的持久化/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `single_session_run.py` | 单会话上下文内连跑，止于 8k token 上限炸 0% | 第 1 章 单会话阶 |
| 2 | `cross_session_snapshot.py` | 断点快照 JSON + 续跑，止于失真率 18% | 第 2 章 跨会话阶 |
| 3 | `cross_day_persist.py` | 冷存 + 一致性哈希校验 + 过夜续跑，漂移率 7% | 第 3 章 跨日阶 |
| 4 | `hybrid_persist_router.py` | 按时间跨度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `breakpoint_chain.py` | 跨日多断点链式追溯，续跑率 100% | 第 5 章 断点链管理 |
| 6 | `cold_store_medium.py` | 冷存介质三策略权衡（本地/远程/云端），续跑率 87% | 第 6 章 冷存介质 |
| 7 | `continuation_rate.py` | 续跑率量化——跨日 100% vs 单会话 0% 核心 KPI | 第 7 章 续跑率 |

## 运行

```bash
cd src/三-Agent之刃/3.12-长程任务Agent：跨日跨会话的持久化
python single_session_run.py
python cross_session_snapshot.py
python cross_day_persist.py
python hybrid_persist_router.py
python breakpoint_chain.py
python cold_store_medium.py
python continuation_rate.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。LLM 调用用模拟实现，生产替换为真实 API。

## 规范

- 每个 .py 独立可运行，不跨文件 import 同项目模块
- 依赖内联：仅依赖标准库（random / hashlib / json）
- 模拟 LLM：random + 固定串替代真实模型推理
- demo 产生非空 stdout 输出

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
