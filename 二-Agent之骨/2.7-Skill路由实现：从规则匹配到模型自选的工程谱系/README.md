# 2.7 Skill 路由实现 — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖路由五档谱系与运维。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `naive_vs_spectrum.py` | 量化五档路由策略在 50 skill 系统上的召回率与成本对比 | 第 1 章 |
| `rule_router.py` | 第一档规则匹配——关键词命中路由 | 第 2 章 |
| `vector_router.py` | 第二档向量检索——embedding 余弦相似度 top-k | 第 3 章 |
| `tiered_router.py` | 第三档分级路由——规则先截向量后补 | 第 4 章 |
| `model_select.py` | 第四档模型自选——向量取 top-k 候选 LLM 从中选 | 第 5 章 |
| `hybrid_router.py` | 第五档混合谱系——按任务难度动态选路由档 | 第 6 章 |
| `route_ops.py` | 路由运维——监控误选率与 skill 描述健康度 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.7-Skill路由实现：从规则匹配到模型自选的工程谱系/
python tiered_router.py       # 查看分级路由（生产最佳实践）
python naive_vs_spectrum.py   # 查看五档谱系对比
python hybrid_router.py       # 查看混合谱系终极甜点
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
