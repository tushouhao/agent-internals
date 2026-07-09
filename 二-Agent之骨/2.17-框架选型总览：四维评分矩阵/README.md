# 2.17 框架选型总览：四维评分矩阵 — 源码说明

> 文章路径：`二-Agent之骨/2.17-框架选型总览：四维评分矩阵/index.md`
> 本目录源码与文章正文内嵌 python 块互补，每个文件独立可运行，不跨文件 import。
> 本篇是卷二收卷篇，承接全卷二 16 篇散点评分，立四维评分矩阵做终极选型。

## 文件清单（7 个）

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `scatter_scores.py` | 卷二 16 篇散点评分回顾 + 收卷困局 | 第 1 章 |
| `matrix_skeleton.py` | 四维评分矩阵骨架（横轴 7 类 × 纬轴 4 维）+ 加权推荐 | 第 2 章 |
| `dim1_ecology.py` | 维一生态成熟度（社区/文档/迭代/绑定四子项） | 第 3 章 |
| `dim2_efficiency.py` | 维二工程效率（上手/配置/调试三子项） | 第 4 章 |
| `dim3_controllability.py` | 维三可控性（源码/状态/定制三子项） | 第 5 章 |
| `dim4_performance.py` | 维四性能（延迟/吞吐/资源三子项） | 第 6 章 |
| `final_decision.py` | 收卷判据（六类场景权重 + 生死级剪枝优先 + 卷三前瞻） | 第 7 章 |

## 运行方式

```bash
# 单文件运行（每个文件独立可跑，不依赖其他文件）
python scatter_scores.py
python matrix_skeleton.py
python dim1_ecology.py
python dim2_efficiency.py
python dim3_controllability.py
python dim4_performance.py
python final_decision.py

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
- 量化数据（7×4=28 格评分/四子项权重/六类场景权重）与正文一致

## 承接关系

- 承接卷二全 16 篇散点评分（2.1-2.5/2.6-2.7/2.8-2.12/2.13/2.14/2.15/2.16）
- 承接 2.15 决策树剪枝规则（生死级剪枝优先）
- 承接 2.16 层级委托（横纵二分：横向选型用矩阵/纵向委托用层级）
- 卷二 17 篇完结，卷三 Agent 之刃 14 篇转「框架内怎么实战」

> 仓库地址：https://github.com/tushouhao/agent-internals
