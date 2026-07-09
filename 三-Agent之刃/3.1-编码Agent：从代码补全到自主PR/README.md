# 3.1 编码 Agent：从代码补全到自主 PR — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖编码 Agent 三级自主性的形式化、补全级上下文工程、修改级跨文件一致性、PR 级多提交序列、SWE-bench 硬墙、三级对照实验、opencode 切片定位。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `autonomy_levels.py` | 三级自主性形式化定义与崩溃模式映射 | 第 1 章 |
| `completion_context.py` | 补全级五源上下文组装与对齐率量化 | 第 2 章 |
| `modification_consistency.py` | 修改级跨文件一致性与影响面分析 | 第 3 章 |
| `pr_sequence.py` | PR 级多提交序列与评审反馈循环 | 第 4 章 |
| `swe_bench_ceiling.py` | SWE-bench 三档分布与破墙要素量化 | 第 5 章 |
| `three_tier_comparison.py` | 三级 Agent 在 100 Issue 上的完成率 vs 解决率对照 | 第 6 章 |
| `opencode_tier_locator.py` | opencode 在三级自主性中的位置定位 | 第 7 章 |

## 运行方式

```bash
cd src/三-Agent之刃/3.1-编码Agent：从代码补全到自主PR/
python three_tier_comparison.py    # 查看三级权衡曲线量化
python swe_bench_ceiling.py        # 查看SWE-bench 50%硬墙分析
python opencode_tier_locator.py    # 查看 opencode 在三级中的定位
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
