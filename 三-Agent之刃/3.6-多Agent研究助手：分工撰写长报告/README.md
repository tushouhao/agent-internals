# 3.6 多 Agent 研究助手：分工撰写长报告 · 源码

> 6 个独立可运行 .py（第 1 章纯理论无源码，其余 6 章各一），每文件含 `if __name__ == "__main__"` demo，不跨文件 import。

| 序 | 文件 | 对应章节 | 功能 |
|---|---|---|---|
| 1 | single_agent_draft.py | 第2章 | naive vs 生产单 Agent 直撰对照（分段扫+先拆纲+分章写+自审） |
| 2 | pipeline_division.py | 第3章 | naive vs 生产流水线分工对照（资料→大纲→正文→校对 链式传递+校验） |
| 3 | parallel_collab.py | 第4章 | naive vs 生产并行协作对照（分章并行+合并+冲突检测+消解+校对） |
| 4 | conflict_resolution.py | 第5章 | naive vs 生产冲突消解对照（术语+风格+引用三类消歧+全局校对） |
| 5 | hybrid_collab_router.py | 第6章 | 混合系统报告判别器（按字数+深度分流三阶+拒拆分护栏） |
| 6 | research_agent_orchestrator.py | 第7章 | 多 Agent 研究助手主调度（整合三阶协作+冲突消解完整混合系统） |

## 运行

```bash
cd src/三-Agent之刃/3.6-多Agent研究助手：分工撰写长报告
python single_agent_draft.py
python pipeline_division.py
python parallel_collab.py
python conflict_resolution.py
python hybrid_collab_router.py
python research_agent_orchestrator.py
```

## 约束

- LLM 用模拟（hash 伪 token 估算 + Agent 写作字典模拟），不调外部 API
- 依赖内联：仅用 collections.Counter，无第三方包
- 量化基线为 150 长报告任务实测值，写在每 demo 输出末
