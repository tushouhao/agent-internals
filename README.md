# 源码索引

> 本目录存放《AI Agent 技术内幕》全部文章的可运行源码，按「卷/文章」两级目录组织。每篇文章的源码可独立运行，含 `if __name__ == "__main__"` demo。

## 目录结构

```
src/
├── 一-Agent之心/      卷一 原理篇源码 (17篇, 已完成)
├── 二-Agent之骨/      卷二 框架篇源码 (17篇, 已完成 17/17, 卷二完结)
├── 三-Agent之刃/      卷三 实战篇源码 (14篇, 待撰写)
└── 四-Agent之盾/      卷四 避坑篇源码 (15篇, 待撰写)
```

## 运行方式

```bash
# 进入某篇文章的源码目录
cd src/一-Agent之心/1.1-Agent的灵魂：从ReAct到自主智能体/

# 运行任意源码文件 (每个文件含 __main__ demo)
python agent_core.py
python react_agent.py
```

## 进度总览

| 卷 | 篇数 | 已完成 | 源码文件数 | 运行验证 |
|---|---|---|---|---|
| 一 · Agent 之心 | 17 | 17 | 113 | 113/113 ✓ |
| 二 · Agent 之骨 | 17 | 0 | - | - |
| 三 · Agent 之刃 | 14 | 0 | - | - |
| 四 · Agent 之盾 | 15 | 0 | - | - |
| **合计** | **63** | **17** | **113** | **113/113 ✓** |

## 源码规范

- 每个文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每个文件含 `if __name__ == "__main__"` demo 块，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），确保单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API
- 每篇文章的源码目录含独立 `README.md` 列出文件清单

## 卷一源码清单

详见 [一-Agent之心/README.md](./一-Agent之心/README.md)

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
