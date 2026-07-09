# 2.9 LangGraph 状态机工程化 — 源码说明

> 本篇 7 个可运行 Python 源码，承接 2.8 链式六短板，看图式抽象如何补上又引入哪些新代价。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_graph.py` | 裸 LangGraph 基线 73% vs 完整 harness 88% 在 50 任务上的完成率对比 | 第 1 章 |
| `state_assembly.py` | State 共享（100% 可见）vs 链式传值（4%）+ 字段契约 bug 三类模式 | 第 2 章 |
| `conditional_fanout.py` | 条件边路由 + 并行扇出 vs 链式串行的延迟/准确率/样板量对比 | 第 3 章 |
| `error_recovery_graph.py` | 节点重试 + 降级边 + 幂等键 vs 链式异常上抛的崩率/降级/副作用对比 | 第 4 章 |
| `checkpointer_resume.py` | MemorySaver/SqliteSaver 三档持久化 + 崩了续跑 + 序列化约束 | 第 5 章 |
| `gate_budget.py` | 边 gate 校验 + 预算回调 StopBudget 软停 vs 链式无护栏无成本 | 第 6 章 |
| `graph_boundary.py` | 图式抽象失效边界四红线判据 + 三类任务完成率基线 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.9-LangGraph：图式编排与状态机工程化/
python naive_vs_graph.py      # 查看裸Graph 73% vs 完整harness 88%
python state_assembly.py      # 查看State共享vs链式+字段契约bug
python graph_boundary.py      # 查看四红线判据与三类任务基线
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟节点 fn 与不稳定节点（教学版），生产使用需替换为真实 LLM API
- 量化数据均按经验文件实测均值校准（裸图基线 73%、手补图 88%、完整 89% 等）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
