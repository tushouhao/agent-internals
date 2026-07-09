# 3.7 工作流编排 Agent：跨系统任务自动化 · 源码

> 6 个独立可运行 .py（第 1 章纯理论无源码，其余 6 章各一），每文件含 `if __name__ == "__main__"` demo，不跨文件 import。

| 序 | 文件 | 对应章节 | 功能 |
|---|---|---|---|
| 1 | single_system_task.py | 第2章 | naive vs 生产单系统任务对照（前置校验+字段映射+执行校验+软重试） |
| 2 | multi_system_chain.py | 第3章 | naive vs 生产多系统串联对照（链式传递+异构映射+链断检测+回滚） |
| 3 | cross_system_orchestrate.py | 第4章 | naive vs 生产跨系统编排对照（动态规划+异构适配+失败补偿） |
| 4 | failure_compensation.py | 第5章 | naive vs 生产失败补偿护栏对照（环关键性+失败类型+降级+回滚） |
| 5 | hybrid_orchestrate_router.py | 第6章 | 混合系统跨度判别器（按系统数+动态性分流三弦+拒编排护栏） |
| 6 | workflow_agent_orchestrator.py | 第7章 | 工作流编排 Agent 主调度（整合三弦+异构适配+失败补偿完整混合系统） |

## 运行

```bash
cd src/三-Agent之刃/3.7-工作流编排Agent：跨系统任务自动化
python single_system_task.py
python multi_system_chain.py
python cross_system_orchestrate.py
python failure_compensation.py
python hybrid_orchestrate_router.py
python workflow_agent_orchestrator.py
```

## 约束

- 系统调用用模拟（CRM/ERP/邮件/短信/礼券字典 + 随机失败），不调真实 API
- 依赖内联：仅用 time/random，无第三方包
- 量化基线为 180 跨系任务实测值，写在每 demo 输出末
