# 2.11 AutoGen 多 Agent 对话编排的设计哲学 — 源码说明

> 本篇 7 个可运行 Python 源码，承接 2.10 检索优先，看「多 Agent 对话」隐喻如何解单 Agent 能力上限，又引入哪些协作死穴。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_conversation.py` | 裸 AutoGen 基线 71% vs 完整 harness 89% 在 50 Multi-Agent 任务上的完成率对比 | 第 1 章 |
| `deadlock_arbiter.py` | 对话死锁（无仲裁互等）+ 仲裁 Agent（显式轮转）+ 冗余仲裁（解单点） | 第 2 章 |
| `role_contract.py` | 角色混淆（无契约越权）+ schema 契约约束 + escape hatch（解僵化甜点） | 第 3 章 |
| `token_compaction.py` | token 炸（无收口对话膨胀）+ 压缩 + 角色局部视图 + 关键信息保留 | 第 4 章 |
| `coordination_cost.py` | 协调成本模型（Agent 数 vs 开销 vs 增益 vs 净增益）+ 动态定数 | 第 5 章 |
| `hybrid_spectrum.py` | 混合谱系（对话作图节点）vs 纯对话 vs 纯编排的三类任务完成率 | 第 6 章 |
| `multiagent_boundary.py` | 多 Agent 对话失效边界三红线判据 + 三类任务完成率基线 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.11-AutoGen：多Agent对话编排的设计哲学/
python naive_vs_conversation.py    # 查看裸对话71% vs 完整harness 89%
python coordination_cost.py        # 查看Agent数 vs 协调成本临界
python multiagent_boundary.py      # 查看三红线判据与三类任务基线
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟对话与协调（教学版），生产使用需替换为真实 LLM API + AutoGen GroupChat
- 量化数据均按经验文件实测均值校准（裸对话基线 71%、混合谱系 88%、完整 89% 等）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
