# 2.12 CrewAI 角色化协作的抽象层级 — 源码说明

> 本篇 7 个可运行 Python 源码，承接 2.11 多 Agent 对话，看「角色化」隐喻如何把对话涌现的角色定义显式化，又引入哪些抽象层级错配。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_crew.py` | 裸 CrewAI 基线 73% vs 完整 harness 89% 在 50 角色化任务上的完成率对比 | 第 1 章 |
| `role_abstraction.py` | Role 抽象失指导（无契约输出散 14%）+ 输出契约 + escape hatch | 第 2 章 |
| `task_abstraction.py` | Task 抽象失灵活（写死步骤僵化 8%）+ 目标导向 + escape hatch | 第 3 章 |
| `crew_abstraction.py` | Crew 协作僵化（sequential 强制串行）+ dynamic + Flow 图式 | 第 4 章 |
| `layer_mismatch.py` | Role/Task/Crew 三层抽象层级错配 + 三层职责契约 + escape hatch | 第 5 章 |
| `hybrid_spectrum.py` | 混合谱系（Crew 作图节点）vs 纯 Crew vs 纯编排的三类任务完成率 | 第 6 章 |
| `crew_boundary.py` | 角色化协作失效边界三红线判据 + 三类任务完成率基线 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.12-CrewAI：角色化协作的抽象层级/
python naive_vs_crew.py        # 查看裸Crew 73% vs 完整harness 89%
python crew_abstraction.py     # 查看sequential/dynamic/Flow 协作僵化
python crew_boundary.py        # 查看三红线判据与三类任务基线
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟角色化协作（教学版），生产使用需替换为真实 LLM API + CrewAI Crew
- 量化数据均按经验文件实测均值校准（裸 Crew 基线 73%、混合谱系 88%、完整 89% 等）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
