# 3.5 浏览器自动化 Agent：Web 任务的长程执行 · 源码

> 6 个独立可运行 .py（第 1 章纯理论无源码，其余 6 章各一），每文件含 `if __name__ == "__main__"` demo，不跨文件 import。

| 序 | 文件 | 对应章节 | 功能 |
|---|---|---|---|
| 1 | single_page_action.py | 第2章 | naive vs 生产单页操作对照（多策略+等待+校验+溯源） |
| 2 | multi_page_flow.py | 第3章 | naive vs 生产多页流程对照（导航链+跨页状态+分段填写+回滚） |
| 3 | long_span_task.py | 第4章 | naive vs 生产长程任务对照（拆多步+断点快照+护栏+续跑校验） |
| 4 | crash_guardrail.py | 第5章 | naive vs 生产反崩溃护栏对照（反弹窗+加载等待+反爬降频+重试计数） |
| 5 | hybrid_span_router.py | 第6章 | 混合系统跨度判别器（按任务特征分流三程+拒执行） |
| 6 | browser_agent_orchestrator.py | 第7章 | 浏览器自动化 Agent 主调度（整合三程+护栏+断点续跑完整混合系统） |

## 运行

```bash
cd src/三-Agent之刃/3.5-浏览器自动化Agent：Web任务的长程执行
python single_page_action.py
python multi_page_flow.py
python long_span_task.py
python crash_guardrail.py
python hybrid_span_router.py
python browser_agent_orchestrator.py
```

## 约束

- 浏览器用模拟（DOM 树/页面字典/崩溃源字典），不调真实 Selenium/Playwright
- 依赖内联：仅用 math/time/json/os/random，无第三方包
- 量化基线为 200 任务实测值，写在每 demo 输出末
- 断点快照写临时文件 `.browser_snap.tmp` / `.long_span_snap.tmp`，完成后自动清理
