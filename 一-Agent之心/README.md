# 卷一 · Agent 之心 — 源码索引

> 17 篇文章的 108 个可运行 Python 源码，全部通过运行时验证（含 `__main__` demo + 非空输出）。

## 源码清单

| 编号 | 文章 | 源码数 | 文件列表 |
|---|---|---|---|
| 1.1 | Agent 的灵魂：从 ReAct 到自主智能体 | 6 | `agent_core` `react_agent` `autonomy_levels` `agent_state` `error_recovery` `agent_checklist` |
| 1.2 | 大模型作为推理引擎 | 9 | `task_classifier` `nlu_evaluator` `reasoning_dispatcher` `syllogism_generator` `verify_inference` `plan_verifier` `citation_verifier` `hallucination_rate` `avail_score` |
| 1.3 | 工具调用原理 | 8 | `parse_tool_call` `tool_schema_design` `parameter_hallucination` `validate_fix_params` `semantic_drift_detector` `tool_call_pipeline` `training_example` `error_stop_loss` |
| 1.4 | 规划机制 I | 7 | `planner` `hierarchical_decomp` `dependency_graph` `cycle_detector` `template_planner` `strategy_selector` `plan_vs_react` |
| 1.5 | 规划机制 II | 7 | `tree_of_thoughts` `bfs_dfs_search` `mcts_search` `pruning_strategy` `reflection_search` `search_complexity` `strategy_selector` |
| 1.6 | 记忆系统 I | 6 | `sliding_window` `context_utilization` `hierarchical_summarizer` `vector_memory` `hybrid_memory` `strategy_selector` |
| 1.7 | 记忆系统 II | 6 | `memory_store` `hnsw_index` `multi_route_retriever` `active_forgetting` `experience_distiller` `memory_integrator` |
| 1.8 | 记忆系统 III | 6 | `write_trigger` `write_filter` `async_batch_writer` `versioned_store` `lock_memory` `quality_monitor` |
| 1.9 | 推理引擎 I：ReAct 范式 | 6 | `react_loop` `cot_vs_react` `step_controller` `termination_detector` `trace_logger` `robust_react` |
| 1.10 | 推理引擎 II：CoT 与自一致性 | 6 | `cot_variants` `depth_controller` `path_diversity` `failure_diagnoser` `weighted_sc` `hybrid_cot_react` |
| 1.11 | 推理引擎 III：思维树 ToT | 6 | `tot_engine` `search_strategies` `node_evaluator` `tot_pruner` `tot_mcts_hybrid` `tot_selector` |
| 1.12 | 推理引擎 IV：反思机制 | 6 | `reflexion_engine` `error_diagnostician` `self_corrector` `reflection_memory` `iteration_optimizer` `reflexion_deployer` |
| 1.13 | 推理引擎 V：自一致性投票 | 6 | `self_consistency` `temperature_optimizer` `voting_strategies` `universal_sc` `sample_number_optimizer` `sc_deployer` |
| 1.14 | 推理引擎 VI：提示工程鲁棒性 | 6 | `example_selector` `example_number_optimizer` `prompt_robustness_tester` `prompt_injection_defender` `prompt_version_control` `prompt_deployment_checklist` |
| 1.15 | Agent 评估与基准测试 | 6 | `agent_evaluator` `benchmark_analyzer` `dynamic_evaluator` `trajectory_evaluator` `human_evaluation_framework` `continuous_evaluation` |
| 1.16 | Agent 安全与对齐 | 6 | `agent_safety_stack` `alignment_paradigms` `action_risk_classifier` `deep_injection_defense` `security_audit_logger` `safety_deployment_checklist` |
| 1.17 | 卷一收尾全貌回顾 | 5 | `volume1_map` `engineering_lessons` `agent_kernel_dataflow` `volume_bridge` `self_assessment` |

**合计**：17 篇 / 108 个源码文件 / 全部运行验证通过 ✓

## 运行方式

```bash
# 进入某篇文章源码目录
cd src/一-Agent之心/1.1-Agent的灵魂：从ReAct到自主智能体/

# 运行任意文件 (含 __main__ demo)
python agent_core.py
python react_agent.py
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API
- 每篇文章目录含独立 `README.md` 列出文件说明

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
