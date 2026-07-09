# 2.10 LlamaIndex 检索优先架构的边界 — 源码说明

> 本篇 7 个可运行 Python 源码，承接 2.9 图式编排，看「检索优先 vs 编排优先」两种哲学差异与各自失效边界。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_retrieval.py` | 裸 LlamaIndex 基线 67% vs 完整 harness 88% 在 50 RAG 任务上的完成率对比 | 第 1 章 |
| `recall_ceiling.py` | 召回上限随 top-k 变化 + 混合检索（向量+BM25+元数据）提升 | 第 2 章 |
| `index_maintenance.py` | 增量索引（hash 检测+差量重建） + 漂移监控（月/3月/6月累计） | 第 3 章 |
| `query_rewrite.py` | 查询改写（sub-question 拆分）+ 改写深度守卫（防失控链） | 第 4 章 |
| `hybrid_spectrum.py` | 混合谱系（检索作图节点）vs 纯检索 vs 纯编排的三类任务完成率 | 第 5 章 |
| `guardrail_cost_rag.py` | RAG 专属护栏（答案溯源校验）+ 检索/推理成本分账双阈值 | 第 6 章 |
| `retrieval_boundary.py` | 检索优先失效边界三红线判据 + 三类任务完成率基线 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.10-LlamaIndexAgent：检索优先架构的边界/
python naive_vs_retrieval.py    # 查看裸索引67% vs 完整harness 88%
python recall_ceiling.py        # 查看召回上限+混合检索
python retrieval_boundary.py   # 查看三红线判据与三类任务基线
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟检索与改写（教学版），生产使用需替换为真实 embedding API + LLM
- 量化数据均按经验文件实测均值校准（裸检索基线 67%、混合谱系 88%、完整 89% 等）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
