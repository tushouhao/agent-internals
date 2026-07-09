# 4.14 终结失控：收尾失败与遗产缺失

> 卷四 · Agent 之盾 · 第十四篇源码

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| no_finalize.py | 收尾失败阶仿真——无收尾校验的产物残率 100% | 第 2 章 |
| legacy_missing.py | 遗产缺失阶仿真——遗产漏检的残留率 18% | 第 3 章 |
| legacy_fallback.py | 遗产漏检降级兜底三策略——保终结残留率降到 3% | 第 3 章 |
| legacy_medium.py | 遗产漏检介质三策略——按任务关键性分流 | 第 3 章 |
| finalize_mismatch.py | 终结失配阶仿真——跨要求适配漏校的失配率 100% | 第 4 章 |
| finalize_adapter.py | 终结失配阶适配检测三档——防失配 | 第 4 章 |
| hybrid_finalize_router.py | 终结失控混合路由器——按终结深度分流三级 | 第 5 章 |
| finalize_residual.py | 终结残留率核心 KPI——三级对照 | 第 5 章 |

## 运行方式

```bash
cd src/四-Agent之盾/4.14-终结失控：收尾失败与遗产缺失
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
