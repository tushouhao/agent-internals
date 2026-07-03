# 1.2 大模型作为推理引擎：能力边界的形式化刻画 — 源码

对应文章：`一-Agent之心/1.2-大模型作为推理引擎：能力边界的形式化刻画/index.md`

## 文件说明

| 文件 | 对应章节 | 说明 |
|---|---|---|
| `task_classifier.py` | 第 1 章 | 推理任务四象限分类器（复杂度 x 知识依赖度） |
| `syllogism_generator.py` | 第 2 章 | 三段论推理题自动生成 |
| `verify_inference.py` | 第 2 章 | 符号推理形式化校验器 |
| `nlu_evaluator.py` | 第 3 章 | NLU 边缘场景评估框架 |
| `plan_verifier.py` | 第 4 章 | 多步规划正确性验证器 |
| `hallucination_rate.py` | 第 5 章 | 幻觉率测量函数 |
| `citation_verifier.py` | 第 5 章 | 引文验证器（交叉验证） |
| `avail_score.py` | 第 6 章 | Avail 可用性评分（0-100） |
| `reasoning_dispatcher.py` | 第 7 章 | 基于 Avail 的推理分发器 |

## 运行要求

- Python 3.8+
- 无第三方依赖（仅标准库）

```bash
# 逐文件验证
python task_classifier.py
python syllogism_generator.py
python verify_inference.py
python nlu_evaluator.py
python plan_verifier.py
python hallucination_rate.py
python citation_verifier.py
python avail_score.py
python reasoning_dispatcher.py
```

## 核心逻辑

这些代码实现了从推理任务分类到推理职责分配的完整链路。文章提出的 Avail 评分是核心工程工具：通过量化任务的复杂度惩罚（-25）、知识开放性惩罚（-15）、符号推理惩罚（-30）等维度，计算每个任务的安全委托评分（0-100），按四档阈值决定走 LLM 直接推理、LLM+Verifier、人机协同还是确定性算法。
---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)

