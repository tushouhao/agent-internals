# 2.4 Loop 工程化 III — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖工具结果异质性、截断甜点、错误清洗、错误传播控制、结构化完整性、回灌时序、compaction 协同。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `result_taxonomy.py` | 工具结果四类异质性分类与处置策略映射 | 第 1 章 |
| `trunc_sweet_point.py` | 大文本截断的甜点——按结果类型选阈值与首尾保留 | 第 2 章 |
| `error_cleaning.py` | 错误清洗——traceback 压为可读建议（37x 压缩） | 第 3 章 |
| `error_propagation.py` | 错误传播控制——计数、降级、熔断三档 | 第 4 章 |
| `structured_complete.py` | 结构化结果回灌——字段标注与完整性信号 | 第 5 章 |
| `timing_modes.py` | 回灌时序——同步、异步、流式三模式 | 第 6 章 |
| `compaction_aware.py` | 回灌与 compaction 协同——压缩感知的回灌 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.4-Loop工程化III：工具结果回灌与错误传播/
python error_cleaning.py         # 查看 traceback 清洗为可读建议
python error_propagation.py      # 查看三档控制节奏
python trunc_sweet_point.py      # 查看三类大文本截断甜点
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
