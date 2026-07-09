# 卷三 · Agent 之刃 — 源码索引

> 14 篇文章的 95 个可运行 Python 源码，全部通过运行时验证（含 `__main__` demo + 非空输出）。

## 源码清单

| 编号 | 文章 | 源码数 | 文件列表 |
|---|---|---|---|
| 3.1 | 编码 Agent：从代码补全到自主 PR | 7 | `autonomy_levels` `completion_context` `modification_consistency` `opencode_tier_locator` `pr_sequence` `swe_bench_ceiling` `three_tier_comparison` |
| 3.2 | 数据分析 Agent：自然语言到 SQL 的可信链路 | 7 | `conclusion_synthesizer` `execution_guards` `four_tier_chain` `four_tier_comparison` `intent_parser` `sql_difficulty_levels` `sql_generator` |
| 3.3 | 客服 Agent：多轮对话中的工单闭环 | 7 | `dialog_state_machine` `escalation_triggers` `faq_recall` `three_tier_comparison` `ticket_extraction` `ticket_loop_formal` `ticket_state_machine` |
| 3.4 | RAG-Agent 混合系统：检索增强的自主决策 | 7 | `autonomous_retrieval` `hybrid_router` `iterative_retrieval` `multi_source_fusion` `naive_single_retrieval` `rag_agent_orchestrator` `reject_guardrail` |
| 3.5 | 浏览器自动化 Agent：Web 任务的长程执行 | 6 | `browser_agent_orchestrator` `crash_guardrail` `hybrid_span_router` `long_span_task` `multi_page_flow` `single_page_action` |
| 3.6 | 多 Agent 研究助手：分工撰写长报告 | 6 | `conflict_resolution` `hybrid_collab_router` `parallel_collab` `pipeline_division` `research_agent_orchestrator` `single_agent_draft` |
| 3.7 | 工作流编排 Agent：跨系统任务自动化 | 6 | `cross_system_orchestrate` `failure_compensation` `hybrid_orchestrate_router` `multi_system_chain` `single_system_task` `workflow_agent_orchestrator` |
| 3.8 | 智能体操作系统：Agent 即服务的架构 | 7 | `fairness_comparison` `hybrid_scheduler` `resource_isolation` `scheduler_agent` `scheduling_metaphor` `service_pool_agent` `single_instance_agent` |
| 3.9 | 嵌入式 Agent：边缘设备的轻量化部署 | 7 | `cloud_full_agent` `continuation_rate` `energy_budget` `hybrid_deployment` `local_pruned_agent` `micro_instant_agent` `resource_pruning_metaphor` |
| 3.10 | 多模态 Agent：图文表格的统一处理 | 7 | `conflict_resolve` `cross_modal_align` `dynamic_recalibrate` `full_modal_fusion` `hybrid_modal_router` `missing_modal_degrade` `unimodal_encode` |
| 3.11 | 协作式 Agent 团队：软件开发流水线 | 7 | `collaborative_team` `conflict_residue_rate` `hybrid_team_router` `pipeline_agents` `pipeline_rollback` `progress_sync` `single_agent_pipeline` |
| 3.12 | 长程任务 Agent：跨日跨会话的持久化 | 7 | `breakpoint_chain` `cold_store_medium` `continuation_rate` `cross_day_persist` `cross_session_snapshot` `hybrid_persist_router` `single_session_run` |
| 3.13 | 开源 Coding Agent 解读：opencode 会话与 loop 切片 | 7 | `cross_session_resume` `full_slice_archive` `hybrid_slice_router` `session_loop` `slice_archive_medium` `slice_completeness_rate` `slice_fallback` |
| 3.14 | 开源 Coding Agent 解读：opencode 多 Agent 与 skill 切片 | 7 | `hybrid_collab_router` `multi_agent` `single_agent` `skill_conflict_fallback` `skill_registry` `skill_registry_medium` `skill_reuse_rate` |

**合计**：14 篇 / 95 个源码文件 / 全部运行验证通过 ✓

## 运行方式

```bash
# 批量验证卷三所有源码
cd src/三-Agent之刃
pass=0; fail=0
for f in 3.*/*.py; do
  if python "$f" > /dev/null 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); echo "✗ $f"; fi
done
echo "通过: $pass, 失败: $fail"
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用与外部 API（教学版），生产使用需替换为真实 LLM API
- 3.5/3.6/3.7 三篇第 1 章为纯理论无源码，每篇 6 个源码文件（其余篇 7 个）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
