# 文件名: modification_consistency.py
# 功能: 修改级跨文件一致性与影响面分析
# 运行: python modification_consistency.py

"""修改级: 跨文件一致性 + 影响面分析 + 测试闭环。

承接 3.1 第 3 章: 跨文件一致性是修改级核心难题,
影响面分析三图合一(符号引用图+测试依赖图+文档扫描)
召回率 89% vs naive 47%。
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple


@dataclass
class FileChange:
    path: str
    diff: str
    reason: str


@dataclass
class ImpactAnalysis:
    """影响面分析: 三图合一。"""
    symbol_refs: Dict[str, List[str]] = field(default_factory=dict)
    test_deps: Dict[str, List[str]] = field(default_factory=dict)
    doc_mentions: Dict[str, List[str]] = field(default_factory=dict)

    def analyze(self, changed_symbol: str) -> List[str]:
        """返回需同步修改的文件列表。"""
        files = set()
        files.update(self.symbol_refs.get(changed_symbol, []))
        for module, tests in self.test_deps.items():
            if changed_symbol.split(".")[0] in module:
                files.update(tests)
        files.update(self.doc_mentions.get(changed_symbol, []))
        return sorted(files)


@dataclass
class ModificationAgent:
    """修改级编码 Agent: 规划-改-测试-修订 loop。"""
    impact: ImpactAnalysis
    changes: List[FileChange] = field(default_factory=list)
    test_runs: int = 0
    max_test_runs: int = 3

    def plan(self, task: str, target_symbol: str) -> List[str]:
        affected = self.impact.analyze(target_symbol)
        print(f"影响面: 改 {target_symbol} 需同步 {len(affected)} 个文件: {affected}")
        return affected

    def apply(self, changes: List[FileChange]) -> str:
        self.changes.extend(changes)
        return f"已写盘 {len(changes)} 个文件"

    def test(self) -> Tuple[bool, str]:
        self.test_runs += 1
        if self.test_runs == 1 and len(self.changes) >= 2:
            return False, "FAIL: test_auth.py::test_login 缺 captcha 参数"
        return True, "all 42 tests passed"

    def fix(self, failure: str) -> List[FileChange]:
        return [FileChange("tests/test_auth.py", "+captcha='ABCD'", "补测试参数")]


def main():
    print("=" * 60)
    print("修改级跨文件一致性 demo")
    print("=" * 60)
    impact = ImpactAnalysis(
        symbol_refs={"auth.login": ["routes.py", "utils.py"]},
        test_deps={"auth": ["tests/test_auth.py", "tests/test_routes.py"]},
        doc_mentions={"auth.login": ["docs/api.md"]},
    )
    agent = ModificationAgent(impact=impact)
    affected = agent.plan("改 login 加 captcha", "auth.login")
    changes = [
        FileChange("auth.py", "def login(u,p,captcha):", "改签名"),
        FileChange("routes.py", "login(u,p,req.captcha)", "改调用"),
        FileChange("docs/api.md", "POST /login +captcha", "改文档"),
    ]
    print(agent.apply(changes))
    for i in range(agent.max_test_runs):
        ok, msg = agent.test()
        print(f"测试轮 {i+1}: {'PASS' if ok else 'FAIL'} - {msg}")
        if ok:
            print("完成: 跨文件一致性达成")
            break
        fixes = agent.fix(msg)
        agent.apply(fixes)
    print("\n影响面召回率:")
    print(f"  naive (只改当前文件): 47%")
    print(f"  三图合一 (LSP+测试+文档): 89%  (+42pp)")


if __name__ == "__main__":
    main()
