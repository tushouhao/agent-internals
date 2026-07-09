# 3.10 多模态 Agent：图文表格的统一处理 — 源码说明

> 专栏：《AI Agent 技术内幕》卷三 · Agent 之刃
> 篇号：3.10
> 正文：`三-Agent之刃/3.10-多模态Agent：图文表格的统一处理/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `unimodal_encode.py` | 三模态独立编道（文本/图像/表格），止于模态内召回 88% | 第 1 章 单模态阶 |
| 2 | `cross_modal_align.py` | 双塔对比对齐（图文 CLIP / 表文 TAP），止于两模态对齐召回 83% | 第 2 章 跨模态阶 |
| 3 | `full_modal_fusion.py` | 三塔门控三模态统一表征，止于齐整召回 79% + 缺模态退化率 0.91 | 第 3 章 全模态阶 |
| 4 | `hybrid_modal_router.py` | 按输入模态构成判别分流三级 + 模态缺失超限拒答 | 第 4 章 混合路由器 |
| 5 | `dynamic_recalibrate.py` | 门控权重动态再校准（降权/升权/置零退化），召回稳态 76% | 第 5 章 动态再校准 |
| 6 | `conflict_resolve.py` | 模态间语义冲突检测三档 + 仲裁消解（投票/降级独答），消解率 91% | 第 6 章 冲突消解 |
| 7 | `missing_modal_degrade.py` | 缺模态退化率量化——门控 0.91 vs naive 0.00 核心 KPI | 第 7 章 缺模态退化率 |

## 运行

```bash
# 全部源码独立可运行，不跨文件 import
cd src/三-Agent之刃/3.10-多模态Agent：图文表格的统一处理
python unimodal_encode.py
python cross_modal_align.py
python full_modal_fusion.py
python hybrid_modal_router.py
python dynamic_recalibrate.py
python conflict_resolve.py
python missing_modal_degrade.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。LLM 调用用模拟实现（hash + random），生产替换为真实模型推理。

## 规范

- 每个 .py 独立可运行，不跨文件 import 同项目模块
- 依赖内联：仅依赖标准库（hashlib / random / collections）
- 模拟 LLM：hash + random 替代真实模型推理
- demo 产生非空 stdout 输出

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
