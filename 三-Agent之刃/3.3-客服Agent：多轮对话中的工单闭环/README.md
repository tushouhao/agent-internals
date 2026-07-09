# 3.3 客服 Agent：多轮对话中的工单闭环 — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖三级工单闭环形式化、单轮 QA 召回、多轮澄清状态机、工单字段抽取、意图升级三触发、三级对照实验、工单状态机与 SLA 跟踪。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `ticket_loop_formal.py` | 三级工单闭环形式化定义与终止条件映射 | 第 1 章 |
| `faq_recall.py` | 单轮 QA：查询改写+多路召回+置信度门控 | 第 2 章 |
| `dialog_state_machine.py` | 多轮澄清：对话状态机三档转移与意图收敛 | 第 3 章 |
| `ticket_extraction.py` | 工单字段抽取四要素+完备性护栏+派单路由 | 第 4 章 |
| `escalation_triggers.py` | 意图升级三触发串联判据 | 第 5 章 |
| `three_tier_comparison.py` | 三级客服 Agent 在 500 对话上的量化对照 | 第 6 章 |
| `ticket_state_machine.py` | 工单状态机+SLA 跟踪+过期预警 | 第 7 章 |

## 运行方式

```bash
cd src/三-Agent之刃/3.3-客服Agent：多轮对话中的工单闭环/
python three_tier_comparison.py    # 查看三级权衡曲线量化
python faq_recall.py               # 查看 FAQ 召回门控 demo
python ticket_state_machine.py     # 查看工单 SLA 跟踪 demo
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
