# 3.8 智能体操作系统：Agent 即服务的架构 — 源码

## 7 个可运行 Python 源码

| 文件 | 对应章节 | 功能 |
|------|----------|------|
| `scheduling_metaphor.py` | 第1章 | 进程三态调度隐喻——三态定义与四轴外扩参数表 |
| `single_instance_agent.py` | 第2章 | 单实例态——无状态 Agent 服务封装与串行压测 |
| `service_pool_agent.py` | 第3章 | 服务池态——多实例负载均衡 + 令牌桶限流 + 熔断 |
| `scheduler_agent.py` | 第4章 | 调度系统态——三级优先级队列 + 资源配额 + 抢占调度 |
| `resource_isolation.py` | 第5章 | 资源隔离——进程隔离 + 配额隔离 + 熔断隔离 |
| `hybrid_scheduler.py` | 第6章 | 混合系统调度器——按任务类型判别分流三态 |
| `fairness_comparison.py` | 第7章 | 公平调度比 vs 吞吐量 200 请求对照实验 |

## 运行方式

```bash
python scheduling_metaphor.py      # 第1章：三态参数表
python single_instance_agent.py    # 第2章：单实例压测
python service_pool_agent.py       # 第3章：服务池压测
python scheduler_agent.py          # 第4章：调度器测试
python resource_isolation.py       # 第5章：隔离测试
python hybrid_scheduler.py         # 第6章：混合分流测试
python fairness_comparison.py      # 第7章：公平性对照
```

## 依赖

仅 Python 标准库，无第三方依赖。
