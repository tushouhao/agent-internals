# 2.14 语义层编排：MCP与工具协议标准化 — 源码说明

> 文章路径：`二-Agent之骨/2.14-语义层编排：MCP与工具协议标准化/index.md`
> 本目录源码与文章正文内嵌 python 块互补，每个文件独立可运行，不跨文件 import。

## 文件清单（7 个）

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `dialect_demo.py` | 四家框架工具方言差异演示（LangChain/AutoGen/Assistants/CrewAI） | 第 1 章 |
| `mcp_trio.py` | MCP 三件套（tools/resources/prompts）语义层骨架 | 第 2 章 |
| `schema_evolve.py` | JSON Schema→OpenAPI→function calling→MCP inputSchema 四代演化 + 双端校验 | 第 3 章 |
| `translation_loss.py` | 协议翻译层三类损耗（语义降级/延迟叠加/能力错配）量化 | 第 4 章 |
| `protocol_lag.py` | 协议滞后量化 + schema 污染（诚实 vs 撒谎）演示 | 第 5 章 |
| `hybrid_spectrum.py` | 四档混合谱系三类任务完成率模拟 + 甜点定位 | 第 6 章 |
| `redline_decision.py` | 四红线串联判据（互操作占比/复用家数/覆盖率/滞后容忍）决策 | 第 7 章 |

## 运行方式

```bash
# 单文件运行（每个文件独立可跑，不依赖其他文件）
python dialect_demo.py
python mcp_trio.py
python schema_evolve.py
python translation_loss.py
python protocol_lag.py
python hybrid_spectrum.py
python redline_decision.py

# 批量验证
for f in *.py; do
  python "$f" > /dev/null 2>&1 && echo "✓ $f" || echo "✗ $f"
done
```

## 依赖

- Python 3.10+（用 `dataclass` slot 与 `typing` 泛型）
- 仅依赖标准库（`dataclasses` / `typing` / `time`），无第三方包

## 与正文的对应

- 正文第 1-7 章各嵌一个节选 python 块（约 20-40 行），展示该章核心逻辑
- 本目录的 7 个 .py 文件是完整可运行版（含 docstring + main + `if __name__ == "__main__"`）
- 量化数据（73% 摊薄、92.7% 压降、-6 个百分点损耗、1.7 月滞后、谱二 88% 甜点、四红线阈值）与正文一致

> 仓库地址：https://github.com/tushouhao/agent-internals
