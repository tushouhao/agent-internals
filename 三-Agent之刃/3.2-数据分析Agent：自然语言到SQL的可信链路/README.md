# 3.2 数据分析 Agent：自然语言到 SQL 的可信链路 — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖四级可信链路形式化、意图解析、SQL 生成、执行校验、结论合成、四级对照实验、三级 SQL 难度。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `four_tier_chain.py` | 四级可信链路形式化定义与校验回滚机制 | 第 1 章 |
| `intent_parser.py` | 意图解析：模糊 NL 到六要素结构化意图 | 第 2 章 |
| `sql_generator.py` | SQL 生成：schema 对齐三因子与 join 推导 BFS | 第 3 章 |
| `execution_guards.py` | 执行校验：三层护栏（空值/异常值/行数） | 第 4 章 |
| `conclusion_synthesizer.py` | 结论合成：溯源标注与反向校验 | 第 5 章 |
| `four_tier_comparison.py` | 四级可信链路 vs naive 在 200 任务上的量化对照 | 第 6 章 |
| `sql_difficulty_levels.py` | 三级 SQL 难度与护栏卡位映射 | 第 7 章 |

## 运行方式

```bash
cd src/三-Agent之刃/3.2-数据分析Agent：自然语言到SQL的可信链路/
python four_tier_comparison.py    # 查看四级 vs naive 量化对照
python sql_generator.py           # 查看 schema 对齐与 join 推导
python execution_guards.py        # 查看三层护栏 demo
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
