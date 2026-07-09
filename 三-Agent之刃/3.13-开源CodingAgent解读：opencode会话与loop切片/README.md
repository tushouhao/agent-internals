# 3.13 开源 Coding Agent 解读：opencode 会话与 loop 切片 — 源码说明

> 专栏：《AI Agent 技术内幕》卷三 · Agent 之刃
> 篇号：3.13
> 正文：`三-Agent之刃/3.13-开源CodingAgent解读：opencode会话与loop切片/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `session_loop.py` | 单会话 ReAct 循环，止于上下文上限炸 0% | 第 1 章 会话内 loop 阶 |
| 2 | `cross_session_resume.py` | 断点快照 + 续跑，止于失真率 22% | 第 2 章 跨会话续阶 |
| 3 | `full_slice_archive.py` | 三维切片归档哈希索引，止于缺失率 15% | 第 3 章 全切片阶 |
| 4 | `hybrid_slice_router.py` | 按切片需求判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `slice_fallback.py` | 切片缺失降级兜底三策略，完备率升到 91% | 第 5 章 降级兜底 |
| 6 | `slice_archive_medium.py` | 归档介质三策略权衡（本地/远程/云端），完备率 87% | 第 6 章 归档介质 |
| 7 | `slice_completeness_rate.py` | 切片完备率量化——全切片 94% vs 会话内 0% 核心 KPI | 第 7 章 切片完备率 |

## 运行

```bash
cd src/三-Agent之刃/3.13-开源CodingAgent解读：opencode会话与loop切片
python session_loop.py
python cross_session_resume.py
python full_slice_archive.py
python hybrid_slice_router.py
python slice_fallback.py
python slice_archive_medium.py
python slice_completeness_rate.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。LLM 调用用模拟实现，生产替换为真实 API。

## 规范

- 每个 .py 独立可运行，不跨文件 import 同项目模块
- 依赖内联：仅依赖标准库（random / hashlib / json）
- 模拟 LLM：random + 固定串替代真实模型推理
- demo 产生非空 stdout 输出

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
