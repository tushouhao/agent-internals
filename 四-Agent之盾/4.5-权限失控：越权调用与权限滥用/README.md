# 4.5 权限失控：越权调用与权限滥用 — 源码说明

> 专栏：《AI Agent 技术内幕》卷四 · Agent 之盾
> 篇号：4.5
> 正文：`四-Agent之盾/4.5-权限失控：越权调用与权限滥用/index.md`

## 文件清单

| # | 文件名 | 功能 | 章对应 |
|---|---|---|---|
| 1 | `unauthorized_call.py` | 无权限调用越权，越权率 100% | 第 1 章 越权调用阶 |
| 2 | `permission_abuse.py` | 过度授予滥用检测，漏检率 18% | 第 2 章 权限滥用阶 |
| 3 | `permission_mismatch.py` | 跨权限适配检测，失配率 100% | 第 3 章 权限失配阶 |
| 4 | `hybrid_perm_router.py` | 按权限深度判别分流三级 + 拒答护栏 | 第 4 章 混合路由器 |
| 5 | `abuse_fallback.py` | 滥用漏检降级兜底三策略，残留率降到 4% | 第 5 章 降级兜底 |
| 6 | `abuse_detect_medium.py` | 滥用检测介质三策略权衡，检测完备率 83% | 第 6 章 检测介质 |
| 7 | `perm_residual.py` | 权限残留率量化——滥用检测 4% vs 越权调用 100% 核心 KPI | 第 7 章 权限残留率 |

## 运行

```bash
cd src/四-Agent之盾/4.5-权限失控：越权调用与权限滥用
python unauthorized_call.py
python permission_abuse.py
python permission_mismatch.py
python hybrid_perm_router.py
python abuse_fallback.py
python abuse_detect_medium.py
python perm_residual.py
```

每个 `.py` 含 `if __name__ == "__main__"` demo，产生非空 stdout 输出。仅依赖标准库（random）。

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
