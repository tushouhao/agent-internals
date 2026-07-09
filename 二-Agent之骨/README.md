# 卷二 · Agent 之骨 — 源码索引

> 17 篇文章的可运行 Python 源码，截至 2.13 已完成 13 篇共 91 个源码文件，全部通过运行时验证（含 `__main__` demo + 非空输出）。

## 源码清单

| 编号 | 文章 | 源码数 | 文件列表 |
|---|---|---|---|
| 2.1 | Harness 工程总论 | 7 | `minimal_harness` `naive_loop` `context_assembler` `tool_scheduler` `error_recovery` `state_persister` `cost_control` |
| 2.2 | Loop 工程化 I | 7 | `state_machine` `loop_signals` `checkpoint` `dead_loop_detector` `termination` `state_diagram` `minimal_loop` |
| 2.3 | Loop 工程化 II | 7 | `context_layers` `compression_strategies` `compaction_pipeline` `tool_extraction` `external_ref` `reversibility` `compaction_verify` |
| 2.4 | Loop 工程化 III | 7 | `heterogeneous_results` `truncation_sweet` `error_cleaning` `error_propagation` `reinject_timing` `compaction_sync` `pipe_verify` |
| 2.5 | 验证护栏 | 7 | `deterministic_check` `llm_judge` `rubric_scoring` `bias_guard` `ab_compare` `double_gate` `adaptive_guard` |
| 2.6 | Skill 工程化 | 7 | `skill_registry` `version_management` `dependency_graph` `lifecycle` `registry_ops` `gradual_migration` `reuse_vs_raw` |
| 2.7 | Skill 路由实现 | 7 | `naive_vs_spectrum` `rule_router` `vector_router` `tiered_router` `model_select` `hybrid_router` `route_ops` |
| 2.8 | LangChain 架构剖析 | 7 | `naive_vs_harness` `context_assembly` `tool_dispatch` `error_recovery` `memory_persistence` `guardrail_cost` `chain_boundary` |
| 2.9 | LangGraph 状态机工程化 | 7 | `naive_vs_graph` `state_assembly` `conditional_fanout` `error_recovery_graph` `checkpointer_resume` `gate_budget` `graph_boundary` |
| 2.10 | LlamaIndex 检索优先架构的边界 | 7 | `naive_vs_retrieval` `recall_ceiling` `index_maintenance` `query_rewrite` `hybrid_spectrum` `guardrail_cost_rag` `retrieval_boundary` |
| 2.11 | AutoGen 多 Agent 对话编排的设计哲学 | 7 | `naive_vs_conversation` `deadlock_arbiter` `role_contract` `token_compaction` `coordination_cost` `hybrid_spectrum` `multiagent_boundary` |
| 2.12 | CrewAI 角色化协作的抽象层级 | 7 | `naive_vs_crew` `role_abstraction` `task_abstraction` `crew_abstraction` `layer_mismatch` `hybrid_spectrum` `crew_boundary` |
| 2.13 | OpenAI Agents SDK 托管式 Agent 的取舍 | 7 | `naive_vs_managed` `state_opacity` `tool_blackbox` `cost_uncontrolled` `vendor_lockin` `hybrid_spectrum` `managed_boundary` |
| 2.14 | 语义层编排：MCP 与工具协议标准化 | 7 | `dialect_demo` `mcp_trio` `schema_evolve` `translation_loss` `protocol_lag` `hybrid_spectrum` `redline_decision` |
| 2.15 | 自研 Harness 决策树：何时不用任何框架 | 7 | `four_rows` `decision_tree` `loop_branch` `managed_branch` `protocol_branch` `pruning_rules` `seven_redlines` |
| 2.16 | Sub-Agent 调度框架：层级委托的工程实现 | 7 | `single_vs_multi` `delegation_protocol` `dispatch_topology` `result_arbitration` `failure_fallback` `ctx_isolation` `depth_limit` |
| 2.17 | 框架选型总览：四维评分矩阵 | 7 | `scatter_scores` `matrix_skeleton` `dim1_ecology` `dim2_efficiency` `dim3_controllability` `dim4_performance` `final_decision` |

## 运行方式

```bash
# 批量验证卷二所有源码
cd src/二-Agent之骨
pass=0; fail=0
for f in 2.*/*.py; do
  if python "$f" > /dev/null 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); echo "✗ $f"; fi
done
echo "通过: $pass, 失败: $fail"
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用与 API 错误（教学版），生产使用需替换为真实 LLM API
- 量化数据均按经验文件实测均值校准

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
