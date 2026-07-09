# 3.14 开源 Coding Agent 解读：opencode 多 Agent 与 skill 切片 — 源码说明

> 专栏：《AI Agent 技术内幕》卷三 · Agent 之刃（收卷篇）
> 篇号：3.14
> 正文：`三-Agent之刃/3.14-开源CodingAgent解读：opencode多Agent与skill切片/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `single_agent.py` | 单 Agent 闭环，止于工具数 ≥15 致选择降 0% | 第 1 章 单 Agent 阶 |
| 2 | `multi_agent.py` | 主子委托协议+回执仲裁四态，止于失真率 22% | 第 2 章 多 Agent 阶 |
| 3 | `skill_registry.py` | skill 动态注册+热加载+复用，止于冲突率 18% | 第 3 章 skill 注册阶 |
| 4 | `hybrid_collab_router.py` | 按协作需求判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `skill_conflict_fallback.py` | 注册冲突降级兜底三策略，复用率升到 91% | 第 5 章 降级兜底 |
| 6 | `skill_registry_medium.py` | 注册表介质三策略权衡（本地/远程/云端），复用率 82% | 第 6 章 注册表介质 |
| 7 | `skill_reuse_rate.py` | skill 复用率量化——skill 注册 93% vs 单 Agent 0% 核心 KPI | 第 7 章 skill 复用率 |

## 运行

```bash
cd src/三-Agent之刃/3.14-开源CodingAgent解读：opencode多Agent与skill切片
python single_agent.py
python multi_agent.py
python skill_registry.py
python hybrid_collab_router.py
python skill_conflict_fallback.py
python skill_registry_medium.py
python skill_reuse_rate.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。LLM 调用用模拟实现，生产替换为真实 API。

## 规范

- 每个 .py 独立可运行，不跨文件 import 同项目模块
- 依赖内联：仅依赖标准库（random / hashlib / json）
- 模拟 LLM：random + 固定串替代真实模型推理
- demo 产生非空 stdout 输出

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
