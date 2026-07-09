# 4.15 Agent 治理总览：从单点到体系的防御纵深

> 卷四 · Agent 之盾 · 第十五篇（收卷篇）源码

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| single_point_benchmark.py | 单点崩阶仿真——十四处孤立修复的残留率均值 2.3% | 第 2 章 |
| cascade_collapse.py | 体系崩阶仿真——连锁坍塌五链路的事故率 100% | 第 3 章 |
| defense_in_depth.py | 治理纵深阶仿真——四层防御纵深的事故率 100%→8% | 第 4 章 |
| depth_fallback.py | 纵深漏检降级兜底三策略——保治理残留率降到 3% | 第 4 章 |
| governance_medium.py | 治理介质三策略——按任务关键性分流 | 第 4 章 |
| hybrid_governance_router.py | 治理混合路由器——按治理深度分流三级 | 第 5 章 |
| governance_residual.py | 治理残留率核心 KPI——三级对照 | 第 5 章 |

## 运行方式

```bash
cd src/四-Agent之盾/4.15-Agent治理总览：从单点到体系的防御纵深
for f in *.py; do
  python "$f" > /dev/null 2>&1 && echo "✓ $f" || echo "✗ $f"
done
```

## 源码规范

- 每个 .py 文件独立可运行，不跨文件 import 同项目模块
- 含 `if __name__ == "__main__"`，demo 产生非空 stdout 输出
- LLM 调用用模拟实现（教学版），生产替换为真实 API
- 依赖内联：仅依赖标准库 + 模拟数据

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
