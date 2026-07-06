# 2.6 Skill 工程化 — 源码说明

> 本篇 7 个可运行 Python 源码，覆盖 skill 注册三元组、版本管理、灰度迁移、依赖图、生命周期、注册表运维、复用收益量化。全部通过运行时验证。

## 文件清单

| 文件 | 功能 | 对应章节 |
|---|---|---|
| `reuse_vs_raw.py` | 量化裸工具调用 vs Skill 化的复用率与 bug 率对比 | 第 1 章 |
| `skill_registry.py` | Skill 注册三元组（语义描述+参数契约+实现代码）与注册表 | 第 2 章 |
| `version_management.py` | SemVer 语义版本号与 breaking change 界定 | 第 3 章 |
| `gradual_migration.py` | MAJOR 升级的灰度迁移——共存/迁移/下线三阶段 | 第 4 章 |
| `dependency_graph.py` | 依赖声明——硬依赖/软依赖/循环检测（DFS） | 第 5 章 |
| `lifecycle.py` | Skill 生命周期——开发/灰度/稳定/弃用四阶段 | 第 6 章 |
| `registry_ops.py` | Skill 注册表运维——监控/告警/审计 | 第 7 章 |

## 运行方式

```bash
cd src/二-Agent之骨/2.6-Skill工程化：注册版本与依赖管理/
python skill_registry.py       # 查看 skill 注册与参数校验
python dependency_graph.py     # 查看循环依赖 DFS 检测
python gradual_migration.py    # 查看灰度迁移三阶段
```

## 源码规范

- 每文件以 `# 文件名` 注释开头，含 `# 运行: python 文件名` 提示
- 每文件含 `if __name__ == "__main__"` demo，可独立运行产生非空输出
- 源码内联依赖（不跨文件 import），单文件可独立运行
- 模拟 LLM 调用（教学版），生产使用需替换为真实 LLM API

---

> **GitHub 仓库**: [github.com/tushouhao/agent-internals](https://github.com/tushouhao/agent-internals)
