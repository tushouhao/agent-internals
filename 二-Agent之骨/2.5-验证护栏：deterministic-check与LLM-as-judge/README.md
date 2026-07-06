# 2.5 验证护栏 — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖错误分类、deterministic 四档、LLM-judge 三要素、双闸叠加、触发频率、重试闭环、自适应护栏。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `error_split.py` | 格式错与语义错两类错误占比与单闸/双闸覆盖率 | 第 1 章 |
| `deterministic_four.py` | deterministic check 四档（正则/类型/AST/Schema）递进校验 | 第 2 章 |
| `llm_judge.py` | LLM-as-judge 三要素——rubric 尺度、swap_order 防偏、compare_ab 相对评分 | 第 3 章 |
| `double_gate.py` | 双闸叠加——deterministic 先短路 LLM-judge 后，成本与延迟对比 | 第 4 章 |
| `trigger_frequency.py` | 护栏触发频率——全检 vs 抽检 vs 关键检对比 | 第 5 章 |
| `guard_retry_loop.py` | 护栏与重试闭环——拦/清洗反馈/限制重试/降级 | 第 6 章 |
| `adaptive_guard.py` | 自适应护栏——按错误率动态调闸频（轻/中/重三档） | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.5-验证护栏：deterministic-check与LLM-as-judge/
python deterministic_four.py    # 查看四档递进校验
python double_gate.py           # 查看双闸叠加与短路
python trigger_frequency.py     # 查看三种触发频率 ROI
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
