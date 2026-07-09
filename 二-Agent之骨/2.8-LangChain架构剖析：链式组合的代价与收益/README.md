# 2.8 LangChain 架构剖析 — 源码说明

> 本篇 7 个可运行 Python 源码，用 2.1 篇六大子系统作透镜逆向拆解 LangChain 链式抽象。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_harness.py` | 裸链基线 vs 完整 harness 在 100 任务上的完成率对比 | 第 1 章 |
| `context_assembly.py` | 链式传值（LinearChain）vs 全局上下文组装（GlobalContextChain）丢失率对比 | 第 2 章 |
| `tool_dispatch.py` | 裸链工具调度 vs SafeToolExecutor 越权/超时/失败/并对比 | 第 3 章 |
| `error_recovery.py` | 链式异常吞噬 vs ErrorRecoveryChain 清洗/计数/降级 | 第 4 章 |
| `memory_persistence.py` | 裸 Memory（buffer 拼接）vs 外存状态（SQLite）跨日回忆对比 | 第 5 章 |
| `guardrail_cost.py` | 裸链无护栏无成本 vs GuardrailChain 护栏+预算阈 | 第 6 章 |
| `chain_boundary.py` | 链式抽象失效边界的三红线判据 + 三类任务完成率基线 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.8-LangChain架构剖析：链式组合的代价与收益/
python naive_vs_harness.py     # 查看裸链41% vs 完整harness~85%完成率
python chain_boundary.py       # 查看三红线判据与三类任务基线
python tool_dispatch.py        # 查看工具调度四缺失的量化代价
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用与 API 错误（教学版），生产使用需替换为真实 LLM API
- 量化数据均按经验文件实测均值校准（裸链基线 41%、完整 harness 89% 等）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
