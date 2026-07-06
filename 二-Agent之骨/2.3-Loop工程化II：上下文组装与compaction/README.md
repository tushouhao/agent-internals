# 2.3 Loop 工程化 II — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖上下文三层结构、四种压缩策略、compaction pipeline、工具抽取、轨迹摘要、引用外存、可逆性。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `three_layers.py` | 上下文三层结构（指令/轨迹/工具）的占比与重要性量化 | 第 1 章 |
| `four_strategies.py` | 四种压缩策略（截断/摘要/抽取/引用）的压缩率与适用场景对比 | 第 2 章 |
| `compaction_pipeline.py` | 分层 compaction pipeline（触发/选择/执行/校验） | 第 3 章 |
| `tool_extraction.py` | 按工具注册的抽取函数（read_file/sql_query/web_search/diff_apply） | 第 4 章 |
| `trajectory_summary.py` | 轨迹层摘要——保近丢远、关键数值锚点、压缩率与语义保留率 | 第 5 章 |
| `reference_external.py` | 引用策略——外存接口、指针格式、拉回决策、语义检索提升准确率 | 第 6 章 |
| `reversibility.py` | 压缩可逆性——外存保证可拉回，对比不可逆截断的累积压错率 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.3-Loop工程化II：上下文组装与compaction/
python compaction_pipeline.py    # 运行分层 compaction demo（80 步任务）
python four_strategies.py        # 查看四种策略压缩率对比
python reversibility.py          # 查看可逆性对比与累积压错率
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
