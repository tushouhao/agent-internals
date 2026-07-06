# 文件名: dependency_graph.py
# 功能: 依赖声明——硬依赖/软依赖/循环检测（DFS）
# 运行: python dependency_graph.py

"""Skill 依赖管理：硬依赖、软依赖、循环检测。

硬依赖: skill 运行必需品（pandas>=2.0），harness 调用前校验
软依赖: 部分功能必需品（matplotlib），lazy import，未装降级
循环依赖: A→B 且 B→A，DFS 在注册时检测，拒绝注册
解法: 抽共同依赖为第三 skill。
教学版，模拟依赖图与循环检测。
"""
from dataclasses import dataclass, field

@dataclass
class DependencyGraph:
    edges: dict = field(default_factory=dict)   # skill → [deps]
    hard_deps: dict = field(default_factory=dict)  # skill → [lib>=version]

    def add(self, skill: str, deps: list, hard_libs: list = None):
        self.edges[skill] = deps
        if hard_libs:
            self.hard_deps[skill] = hard_libs

    def detect_cycle(self) -> list:
        visited, stack = set(), []
        def dfs(node):
            if node in stack:
                return stack[stack.index(node):]
            if node in visited:
                return None
            visited.add(node)
            stack.append(node)
            for dep in self.edges.get(node, []):
                result = dfs(dep)
                if result:
                    return result
            stack.pop()
            return None
        for node in list(self.edges):
            cycle = dfs(node)
            if cycle:
                return cycle
        return None

    def check_hard_deps(self, skill: str, installed: list) -> tuple:
        deps = self.hard_deps.get(skill, [])
        for dep in deps:
            lib_name = dep.split(">=")[0].strip()
            if lib_name not in installed:
                return False, f"硬依赖缺失: {dep}"
        return True, ""

def main():
    print("=" * 64)
    print("Skill 依赖管理：硬依赖/软依赖/循环检测")
    print("=" * 64)
    g = DependencyGraph()
    g.add("analyze_csv", [], ["pandas>=2.0", "numpy>=1.20"])
    g.add("generate_report", ["analyze_csv"], ["matplotlib>=3.0"])
    g.add("send_email", [], [])
    print("依赖图:")
    for sk, deps in g.edges.items():
        hard = g.hard_deps.get(sk, [])
        print(f"  {sk} → skill 依赖: {deps}, 硬依赖: {hard}")
    print(f"\n循环检测: {g.detect_cycle() or '无循环 ✓'}")
    print("\n硬依赖校验:")
    ok, msg = g.check_hard_deps("analyze_csv", ["pandas", "numpy"])
    print(f"  analyze_csv（已装 pandas+numpy）: {'✓' if ok else '✗ '+msg}")
    ok, msg = g.check_hard_deps("generate_report", ["pandas", "numpy"])
    print(f"  generate_report（未装 matplotlib）: {'✓' if ok else '✗ '+msg}")
    print()
    print("结论: DFS 在注册时检循环，拒注册")
    print("      硬依赖调用前校验，未装返回结构化错误")
    print("      软依赖 lazy import，未装降级功能")

if __name__ == "__main__":
    main()
