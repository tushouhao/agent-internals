# 1.11 分岔的森林：思维树 ToT 与全局搜索 — 源码

| 文件 | 说明 |
|---|---|
| `tot_engine.py` | ToT 四阶段循环引擎 |
| `search_strategies.py` | BFS/DFS/Beam 三种搜索策略 |
| `node_evaluator.py` | 节点评估函数（绝对/相对/投票） |
| `tot_pruner.py` | 剪枝策略（阈值/重复/停滞） |
| `tot_mcts_hybrid.py` | ToT+MCTS 融合引擎 |
| `tot_selector.py` | ToT 适用性选择器 |

**GitHub**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
