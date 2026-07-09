# 2.13 OpenAI Agents SDK 托管式 Agent 的取舍 — 源码说明

> 本篇 7 个可运行 Python 源码，承接 2.12 角色化协作，看「托管式」隐喻如何把框架的工程负担转给云，又引入哪些托管即失控的边界。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_managed.py` | 裸 Assistants API 基线 76% vs 完整 harness 89% 在 50 托管任务上的完成率对比 | 第 1 章 |
| `state_opacity.py` | 托管状态不透明（黑盒 loop 调试盲区 17%）+ Run Steps API + 本地镜像 | 第 2 章 |
| `tool_blackbox.py` | 托管工具黑盒（function calling 失控 30%）+ 护栏 + 按需检 | 第 3 章 |
| `cost_uncontrolled.py` | 托管成本失控（Runs 自动多轮 2.3× 预算）+ max_steps + 预算回调 | 第 4 章 |
| `vendor_lockin.py` | 托管锁锁定（vendor lock-in 280 行）+ 抽象层 + 本地镜像 + 开标协议 | 第 5 章 |
| `hybrid_spectrum.py` | 混合谱系（托管作自研节点）vs 纯托管 vs 纯自研的三类任务完成率 | 第 6 章 |
| `managed_boundary.py` | 托管式 Agent 失效边界三红线判据 + 三类任务完成率基线 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.13-OpenAIAgentsSDK：托管式Agent的取舍/
python naive_vs_managed.py        # 查看裸托管76% vs 完整harness 89%
python cost_uncontrolled.py       # 查看托管成本失控 + max_steps
python managed_boundary.py        # 查看三红线判据与三类任务基线
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟托管 Runs（教学版），生产使用需替换为真实 OpenAI Assistants API
- 量化数据均按经验文件实测均值校准（裸托管基线 76%、混合谱系 88%、完整 89% 等）

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
