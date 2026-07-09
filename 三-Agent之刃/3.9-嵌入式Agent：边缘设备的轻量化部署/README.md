# 3.9 嵌入式 Agent：边缘设备的轻量化部署 — 源码

## 7 个可运行 Python 源码

| 文件 | 对应章节 | 功能 |
|------|----------|------|
| `resource_pruning_metaphor.py` | 第1章 | 资源三阶裁剪隐喻——三阶部署参数与四轴外扩 |
| `cloud_full_agent.py` | 第2章 | 云端全量阶——边缘转发 + LRU 缓存 + 离线降级 |
| `local_pruned_agent.py` | 第3章 | 本地裁剪阶——7B→1.5B 裁剪 + INT8 量化 + 精度校准 |
| `micro_instant_agent.py` | 第4章 | 微端即用阶——蒸馏 + INT4 量化 + 50ms 硬实时 |
| `hybrid_deployment.py` | 第5章 | 混合部署调度——微端→边缘→云端分流 + 断网守护 |
| `energy_budget.py` | 第6章 | 能耗预算管理——推理控制 + 睡眠调度 + 预算管理 |
| `continuation_rate.py` | 第7章 | 续航完成率 vs 精度 200 任务对照实验 |

## 运行方式

```bash
python resource_pruning_metaphor.py   # 第1章：三阶参数表
python cloud_full_agent.py            # 第2章：云端全量压测
python local_pruned_agent.py          # 第3章：本地裁剪压测
python micro_instant_agent.py         # 第4章：微端硬实时压测
python hybrid_deployment.py           # 第5章：混合分流压测
python energy_budget.py               # 第6章：能耗预算压测
python continuation_rate.py           # 第7章：续航完成率对照
```

## 依赖

仅 Python 标准库，无第三方依赖。
