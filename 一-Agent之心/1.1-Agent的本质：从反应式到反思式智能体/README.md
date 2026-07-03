# 1.1 Agent 的灵魂：从反应式到反思式智能体 — 源码

本文配套的可运行源码。对应文章：`1.1-Agent的本质：从反应式到反思式智能体/index.md`

## 文件说明

| 文件 | 对应文章章节 | 说明 | 运行 |
|---|---|---|---|
| `agent.py` | 第 1 章 | Agent 最小骨架（S-D-A-E 四要素） | `python agent.py` |
| `pomdp_agent.py` | 第 1 章 | POMDP 扩展：信念状态维护 | `python pomdp_agent.py` |
| `reactive_agent.py` | 第 2 章 | 反应式决策：查表映射 + 规则表 | `python reactive_agent.py` |
| `compress_obs.py` | 第 2 章 | 感知特征压缩（高维→低维） | `python compress_obs.py` |
| `bdi_agent.py` | 第 3 章 | BDI 模型（Belief-Desire-Intention） | `python bdi_agent.py` |
| `hybrid_agent.py` | 第 4 章 | 混合式架构：反应层+慎思层协同 | `python hybrid_agent.py` |
| `react_loop.py` | 第 5 章 | ReAct 循环（思考-行动-观察） | `python react_loop.py` |
| `reflective_agent.py` | 第 6 章 | 反思式 Agent：自评+修正 | `python reflective_agent.py` |
| `state_machine.py` | 第 7 章 | 状态机做控制流、LLM 做数据流 | `python state_machine.py` |

## 运行要求

- Python 3.8+
- 无第三方依赖（仅使用标准库）

## 使用方式

```bash
# 运行全部文件验证
python agent.py
python reactive_agent.py
python pomdp_agent.py
python compress_obs.py
python bdi_agent.py
python hybrid_agent.py
python react_loop.py
python reflective_agent.py
python state_machine.py
```

## 代码说明

每份代码文件结构一致：

1. **核心实现** — 文章中的类/函数定义（可直接用于项目原型）
2. **`if __name__ == "__main__"`** — 可运行的演示用例，展示核心逻辑的执行流程

这些代码是教学性骨架实现，旨在展示 Agent 六种架构的核心设计模式，而非生产级完整实现。生产部署需要根据具体场景添加错误处理、日志、性能监控等工程化组件。
---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)

