# 2.1 Harness 工程总论 — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖 harness 六大子系统与决策判据。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `harness_scope.py` | 量化裸 loop vs 完整 harness 在不同步数上的成功率差距 | 第 1 章 |
| `six_subsystems.py` | 六大子系统职责拆解与崩溃防护映射 | 第 2 章 |
| `crash_reproduction.py` | 复现裸 loop 四类典型崩溃的量化数据 | 第 3 章 |
| `minimal_harness.py` | 200 行实现六大子系统的最小可用 harness 骨架 | 第 4 章 |
| `context_assembly.py` | 上下文组装子系统：naive 截断 vs 分层压缩对比 | 第 4 章深化 |
| `framework_xray.py` | 逆向拆解 LangChain/LangGraph/AutoGen 对 harness 的覆盖度 | 第 5 章 |
| `build_vs_buy.py` | 自研 vs 用框架的三条判据决策器 | 第 6 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.1-Harness工程总论：模型之外的完整基础设施/
python minimal_harness.py    # 运行完整 harness 骨架 demo
python harness_scope.py      # 查看成功率量化对比
python build_vs_buy.py       # 用决策器评估你的场景
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
