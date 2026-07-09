# 4.1 规划失败：子目标爆炸与死循环 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾（开卷篇）
> 篇号：4.1
> 正文：`四-Agent之盾/4.1-规划失败：子目标爆炸与死循环/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `single_goal_fail.py` | 单目标规划止于工具断，完成率 0% | 第 1 章 单目标失败阶 |
| 2 | `subgoal_explosion.py` | 子目标拆分+依赖图爆炸，收敛率 0% | 第 2 章 子目标爆炸阶 |
| 3 | `death_loop.py` | 环依赖+环漏检，死循环率 97% 残留 3% | 第 3 章 死循环阶 |
| 4 | `hybrid_plan_router.py` | 按规划深度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `loop_fallback.py` | 环漏检降级兜底三策略，残留率降到 1% | 第 5 章 降级兜底 |
| 6 | `cycle_detect_medium.py` | 环检测介质三策略权衡，检测完备率 83% | 第 6 章 环检测介质 |
| 7 | `death_loop_residual.py` | 死循环残留率量化——死循环检测 3% vs 单目标 100% 核心 KPI | 第 7 章 死循环残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.1-规划失败：子目标爆炸与死循环
python single_goal_fail.py
python subgoal_explosion.py
python death_loop.py
python hybrid_plan_router.py
python loop_fallback.py
python cycle_detect_medium.py
python death_loop_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。LLM 调用用模拟实现，生产替换为真实 API。

## 规范

- 每个 .py 独立可运行，不跨文件 import 同项目模块
- 依赖内联：仅依赖标准库（random）
- 模拟 LLM：random + 固定串替代真实模型推理
- demo 产生非空 stdout 输出

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
