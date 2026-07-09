# 2.15 自研 Harness 决策树：何时不用任何框架 — 源码说明

> 文章路径：`二-Agent之骨/2.15-自研Harness决策树：何时不用任何框架/index.md`
> 本目录源码与文章正文内嵌 python 块互补，每个文件独立可运行，不跨文件 import。

## 文件清单（7 个）

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `four_rows.py` | 框架生态四横排对照表生成（托管/框架内/协议层/全自研） | 第 1 章 |
| `decision_tree.py` | 决策树根→枝→叶三层骨架 + 可遍历接口 | 第 2 章 |
| `loop_branch.py` | 第一岔 loop 自研 vs 托管决策 + 工程量拆分（承接 2.1-2.5） | 第 3 章 |
| `managed_branch.py` | 第二岔托管厂商三家对照（OpenAI/Anthropic/Bedrock）+ 崩点侧重分流 | 第 4 章 |
| `protocol_branch.py` | 第三岔 MCP 协议层承接岔（引用 2.14 四红线不重拆） | 第 5 章 |
| `pruning_rules.py` | 决策树剪枝规则（三类不该自研 + 三类不该托管 ROI 倒挂） | 第 6 章 |
| `seven_redlines.py` | 七串联判据决策（根2+三枝3+剪枝2）+ 生死级剪枝优先 | 第 7 章 |

## 运行方式

```bash
# 单文件运行（每个文件独立可跑，不依赖其他文件）
python four_rows.py
python decision_tree.py
python loop_branch.py
python managed_branch.py
python protocol_branch.py
python pruning_rules.py
python seven_redlines.py

# 批量验证
for f in *.py; do
  python "$f" > /dev/null 2>&1 && echo "✓ $f" || echo "✗ $f"
done
```

## 依赖

- Python 3.10+（用 `dataclass` slot 与 `typing` 泛型）
- 仅依赖标准库（`dataclasses` / `typing`），无第三方包

## 与正文的对应

- 正文第 1-7 章各嵌一个节选 python 块（约 20-40 行），展示该章核心逻辑
- 本目录的 7 个 .py 文件是完整可运行版（含 docstring + main + `if __name__ == "__main__"`）
- 量化数据（四横排工程量梯度/270 行溢价/350 行自研/80 行托管/180 行 MCP 谱二/七红线阈值）与正文一致

## 承接关系

- 承接卷二 2.1-2.5 loop 工程四部曲（loop_branch 子件拆分）
- 承接卷二 2.13 托管式四崩点（managed_branch 崩点侧重）
- 承接卷二 2.14 四红线判据（protocol_branch 承接岔引用不重拆）
- 下一篇 2.16 Sub-Agent 调度框架承接本篇叶节点「自研 harness」内部层级委托

> 仓库地址：https://github.com/tushouhao/agent-internals
