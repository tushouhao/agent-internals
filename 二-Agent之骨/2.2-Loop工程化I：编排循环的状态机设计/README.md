# 2.2 Loop 工程化 I — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖 loop 状态机设计、信号驱动、checkpoint、死循环检测、三类终止、状态图扩展。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `while_vs_state.py` | 对比裸 while 循环与显式状态机在 12 类边界场景上的应对能力 | 第 1 章 |
| `seven_state_machine.py` | 7 状态 5 边的生产级 loop 状态机骨架 | 第 2 章 |
| `transition_signals.py` | 三类信号（内部/外部/阈值）驱动状态转换的优先级与触发统计 | 第 3 章 |
| `checkpoint_resume.py` | 状态机 loop 的 checkpoint 与崩溃续跑工程 | 第 4 章 |
| `loop_detection.py` | 死循环检测——轨迹指纹与降级处置 | 第 5 章 |
| `three_terminations.py` | 三类终止条件（成功/失败/熔断）的下游处置 | 第 6 章 |
| `fork_merge_graph.py` | 状态图（分叉/合并/回跳）的扩展能力演示 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.2-Loop工程化I：编排循环的状态机设计/
python seven_state_machine.py   # 运行 7 状态状态机 demo
python checkpoint_resume.py     # 查看 checkpoint 续跑耗时对比
python loop_detection.py        # 查看死循环检测与降级
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
