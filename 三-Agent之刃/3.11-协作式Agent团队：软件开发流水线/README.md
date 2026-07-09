# 3.11 协作式 Agent 团队：软件开发流水线 — 源码说明

> 专栏：《AI Agent 技术内幕》卷三 · Agent 之刃
> 篇号：3.11
> 正文：`三-Agent之刃/3.11-协作式Agent团队：软件开发流水线/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `single_agent_pipeline.py` | 单 Agent 独揽全流程，止于上下文上限炸 41% | 第 1 章 单 Agent 阶 |
| 2 | `pipeline_agents.py` | 编码/测试/部署串三，接口契约 JSON 链式传递，止于失配 22% | 第 2 章 流水线阶 |
| 3 | `collaborative_team.py` | 增架构 Agent 协调，冲突三档仲裁，止于残留率 9% | 第 3 章 协作团队阶 |
| 4 | `hybrid_team_router.py` | 按任务阶段数判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `pipeline_rollback.py` | 流水线中途崩溃分阶段回滚，回滚成功率 87% | 第 5 章 回滚护栏 |
| 6 | `progress_sync.py` | Agent 间进度总线广播订阅，空等率降至 0% | 第 6 章 进度同步 |
| 7 | `conflict_residue_rate.py` | 冲突残留率量化——协作团队 9% vs 流水线 67% 核心 KPI | 第 7 章 冲突残留率 |

## 运行

```bash
cd src/三-Agent之刃/3.11-协作式Agent团队：软件开发流水线
python single_agent_pipeline.py
python pipeline_agents.py
python collaborative_team.py
python hybrid_team_router.py
python pipeline_rollback.py
python progress_sync.py
python conflict_residue_rate.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。LLM 调用用模拟实现，生产替换为真实 API。

## 规范

- 每个 .py 独立可运行，不跨文件 import 同项目模块
- 依赖内联：仅依赖标准库（random / collections）
- 模拟 LLM：random 替代真实模型推理
- demo 产生非空 stdout 输出

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
