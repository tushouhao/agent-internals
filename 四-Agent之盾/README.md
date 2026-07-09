# 卷四 · Agent 之盾 — 源码索引

> 15 篇文章的 112 个可运行 Python 源码，全部通过运行时验证（含 `__main__` demo + 非空输出）。

## 源码清单

| 编号 | 文章 | 源码数 | 文件列表 |
|---|---|---|---|
| 4.1 | 规划失败：子目标爆炸与死循环 | 7 | `single_goal_fail` `subgoal_explosion` `death_loop` `hybrid_plan_router` `loop_fallback` `cycle_detect_medium` `death_loop_residual` |
| 4.2 | 工具调用失败：参数幻觉与语义漂移 | 7 | `param_hallucination` `semantic_drift` `drift_residual` `tool_mismatch` `drift_detect_medium` `drift_fallback` `hybrid_call_router` |
| 4.3 | 上下文崩溃：窗口耗尽与信息丢失 | 7 | `window_exhaust` `info_loss` `info_residual` `key_detect_medium` `key_fallback` `truncation_recovery` `hybrid_ctx_router` |
| 4.4 | 成本失控：预算耗尽与成本爆炸 | 7 | `budget_exhaust` `cost_explosion` `cost_mismatch` `cost_residual` `spike_detect_medium` `spike_fallback` `hybrid_cost_router` |
| 4.5 | 权限失控：越权调用与权限滥用 | 7 | `unauthorized_call` `permission_abuse` `permission_mismatch` `perm_residual` `abuse_detect_medium` `abuse_fallback` `hybrid_perm_router` |
| 4.6 | 质量失控：产物降级与质量退化 | 7 | `artifact_degrade` `quality_decay` `quality_mismatch` `quality_residual` `decay_detect_medium` `decay_fallback` `hybrid_quality_router` |
| 4.7 | 并发失控：竞态冲突与死锁图谱 | 7 | `race_conflict` `deadlock_graph` `concurrency_mismatch` `concurrency_residual` `deadlock_detect_medium` `deadlock_fallback` `hybrid_concurrency_router` |
| 4.8 | 协作失控：消息错序与协同失序 | 7 | `message_disorder` `coordination_disorder` `collaboration_mismatch` `collab_residual` `disorder_detect_medium` `disorder_fallback` `hybrid_collab_router` |
| 4.9 | 可观测失控：盲飞运行与诊断缺失 | 7 | `blind_flying` `diagnosis_missing` `observable_mismatch` `observable_residual` `diagnosis_detect_medium` `diagnosis_fallback` `hybrid_obs_router` |
| 4.10 | 降级失控：兜底失效与兜底滥用 | 7 | `fallback_failure` `fallback_abuse` `degrade_mismatch` `degrade_residual` `abuse_detect_medium` `abuse_fallback` `hybrid_degrade_router` |
| 4.11 | 进化失控：策略僵化与适应缺失 | 7 | `strategy_rigid` `adaptation_missing` `evolve_mismatch` `evolve_residual` `adaptation_detect_medium` `adaptation_fallback` `hybrid_evolve_router` |
| 4.12 | 记忆失控：遗忘循环与积累失效 | 7 | `forget_loop` `accumulate_failure` `memory_mismatch` `memory_residual` `failure_detect_medium` `failure_fallback` `hybrid_memory_router` |
| 4.13 | 反思失控：自省失效与元认知缺失 | 7 | `introspect_failure` `metacog_missing` `reflect_mismatch` `reflect_residual` `miss_detect_medium` `miss_fallback` `hybrid_reflect_router` |
| 4.14 | 终结失控：收尾失败与遗产缺失 | 8 | `no_finalize` `legacy_missing` `legacy_fallback` `legacy_medium` `finalize_mismatch` `finalize_adapter` `hybrid_finalize_router` `finalize_residual` |
| 4.15 | Agent 治理总览：从单点到体系的防御纵深 | 7 | `single_point_benchmark` `cascade_collapse` `defense_in_depth` `depth_fallback` `governance_medium` `governance_residual` `hybrid_governance_router` |

**合计**：15 篇 / 112 个源码文件 / 全部运行验证通过 ✓

## 运行方式

```bash
# 批量验证卷四所有源码
cd src/四-Agent之盾
pass=0; fail=0
for f in 4.*/*.py; do
  if python "$f" > /dev/null 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); echo "✗ $f"; fi
done
echo "通过: $pass, 失败: $fail"
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用与外部 API（教学版），生产使用需替换为真实 LLM API
- 4.14 因遗产缺失阶拆三个子阶，源码 8 个（其余篇 7 个）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
