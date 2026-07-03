# 1.3 工具的语法与语义：从函数签名到对齐调用 — 源码

对应文章：`一-Agent之心/1.3-工具调用原理：从函数签名到语义对齐/index.md`

## 文件说明

| 文件 | 对应章节 | 说明 |
|---|---|---|
| `parse_tool_call.py` | 第 1 章 | 工具调用解析器（JSON 提取与校验） |
| `training_example.py` | 第 2 章 | Function Calling 训练数据格式示例 |
| `semantic_drift_detector.py` | 第 3 章 | 语义漂移检测器（基于嵌入 + 邻居对比） |
| `parameter_hallucination.py` | 第 4 章 | 参数幻觉三种典型案例 |
| `validate_fix_params.py` | 第 4 章 | 参数幻觉检测与自动修复 |
| `tool_schema_design.py` | 第 5 章 | 好的 vs 差的工具描述对比 |
| `tool_call_pipeline.py` | 第 6 章 | 生产级 6 阶段工具调用管线 |
| `error_stop_loss.py` | 第 7 章 | 工具调用错误的止损策略 |

## 运行要求

- Python 3.8+
- 无第三方依赖

```bash
python parse_tool_call.py
python training_example.py
python semantic_drift_detector.py
python parameter_hallucination.py
python validate_fix_params.py
python tool_schema_design.py
python tool_call_pipeline.py
python error_stop_loss.py
```

## 核心逻辑

工具调用的核心矛盾：LLM 的工具调用不是程序执行而是文本生成。本文的代码实现了从解析、校验、修复到执行的完整管线，以及语义漂移检测和止损策略两个关键防御组件。
---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)

