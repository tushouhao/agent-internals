# 2.16 Sub-Agent 调度框架：层级委托的工程实现 — 源码说明

> 文章路径：`二-Agent之骨/2.16-Sub-Agent调度框架：层级委托的工程实现/index.md`
> 本目录源码与文章正文内嵌 python 块互补，每个文件独立可运行，不跨文件 import。

## 文件清单（7 个）

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `single_vs_multi.py` | 单 Agent 闭环三崩点量化 + 多 Agent 委托动机 | 第 1 章 |
| `delegation_protocol.py` | 委托协议三件套（task/ctx/budget）序列化契约 | 第 2 章 |
| `dispatch_topology.py` | 串行/并行/树状三种委托拓扑延迟与合并 | 第 3 章 |
| `result_arbitration.py` | 子 Agent 回执四态判据（完成/部分/失败/越界）+ 仲裁 | 第 4 章 |
| `failure_fallback.py` | 四类失败兜底（超时/异常/越界/资源耗尽）+ 代价量化 | 第 5 章 |
| `ctx_isolation.py` | 上下文三层边界 + 三类泄漏防线 | 第 6 章 |
| `depth_limit.py` | 委托链深度红线 ≤3 + depth/budget/cycle 三 guard | 第 7 章 |

## 运行方式

```bash
# 单文件运行（每个文件独立可跑，不依赖其他文件）
python single_vs_multi.py
python delegation_protocol.py
python dispatch_topology.py
python result_arbitration.py
python failure_fallback.py
python ctx_isolation.py
python depth_limit.py

# 批量验证
for f in *.py; do
  python "$f" > /dev/null 2>&1 && echo "✓ $f" || echo "✗ $f"
done
```

## 依赖

- Python 3.10+（用 `dataclass` slot 与 `typing` 泛型）
- 仅依赖标准库（`dataclasses` / `typing` / `copy`），无第三方包

## 与正文的对应

- 正文第 1-7 章各嵌一个节选 python 块（约 20-40 行），展示该章核心逻辑
- 本目录的 7 个 .py 文件是完整可运行版（含 docstring + main + `if __name__ == "__main__"`）
- 量化数据（三崩点阈值/三件套工程量/三拓扑延迟模型/四态判据/四类代价/三层边界/深度红线 ≤3）与正文一致

## 承接关系

- 承接卷二 2.15 决策树叶节点「自研 harness」的单 Agent 闭环做纵向扩展
- 承接卷二 2.2/2.4/2.6 三件套（loop 状态机/工具回灌/Skill 注册）做上下文隔离
- 承接卷二 2.5 验证护栏的双轨校验（deterministic + LLM-judge）做四态判据
- 承接卷二 2.9 图式分支并行思路向多 Agent 维度推广做三拓扑延迟模型
- 下一篇 2.17 框架选型总览承接本篇层级委托 + 2.15 决策树 + 全卷二 16 篇，立四维评分矩阵做终极选型收卷

> 仓库地址：https://github.com/tushouhao/agent-internals
