# 3.4 RAG-Agent 混合系统：检索增强的自主决策 · 源码

> 7 个独立可运行 .py，每文件含 `if __name__ == "__main__"` demo，不跨文件 import。

| 序 | 文件 | 对应章节 | 功能 |
|---|---|---|---|
| 1 | naive_single_retrieval.py | 第2章 | naive vs 生产单检索对照（归一化+多路+重排+引用） |
| 2 | iterative_retrieval.py | 第3章 | naive vs 生产迭代检索对照（改写+多轮+去重+覆盖检查） |
| 3 | autonomous_retrieval.py | 第4章 | naive vs 生产自主检索对照（分类+路由+门控+拒答） |
| 4 | multi_source_fusion.py | 第5章 | naive vs 生产多源融合对照（拆子问+加权+截断+双引用） |
| 5 | reject_guardrail.py | 第6章 | naive vs 生产拒答护栏对照（门控+覆盖+多源齐全+建议） |
| 6 | hybrid_router.py | 第7章 | 混合系统路由器（按问题特征分流三级+拒答） |
| 7 | rag_agent_orchestrator.py | 总结 | RAG-Agent 主调度器（整合三级+多源+拒答完整混合系统） |

## 运行

```bash
cd src/三-Agent之刃/3.4-RAG-Agent混合系统：检索增强的自主决策
python naive_single_retrieval.py
python iterative_retrieval.py
python autonomous_retrieval.py
python multi_source_fusion.py
python reject_guardrail.py
python hybrid_router.py
python rag_agent_orchestrator.py
```

## 约束

- LLM 用模拟（hash 伪 embedding + 简化 BM25），不调外部 API
- 依赖内联：仅用 math/hashlib/re，无第三方包
- 量化基线为 300 任务实测值，写在每 demo 输出末
