# dependency_graph
# 运行: python dependency_graph.py

class DependencyGraph:
    """子目标依赖图"""
    def __init__(self):
        self.nodes = {}     # name -> Subgoal
        self.edges = {}     # name -> [dependencies]

    def add_subgoal(self, name, action, depends_on=None):
        self.nodes[name] = {"action": action, "status": "pending"}
        self.edges[name] = depends_on or []

    def mark_done(self, name):
        if name in self.nodes:
            self.nodes[name]["status"] = "done"

    def get_ready(self):
        """返回所有前置依赖已完成的子目标"""
        ready = []
        for name, deps in self.edges.items():
            if self.nodes[name]["status"] == "pending":
                if all(self.nodes[d]["status"] == "done" for d in deps):
                    ready.append(name)
        return ready

    def detect_cycle(self):
        """检测环：使用 DFS"""
        visited = set()
        path = set()

        def dfs(node):
            if node in path:
                return True  # 发现环
            if node in visited:
                return False
            visited.add(node)
            path.add(node)
            for n, deps in self.edges.items():
                if node in deps:
                    if dfs(n):
                        return True
            path.remove(node)
            return False

        for node in self.nodes:
            if dfs(node):
                return True, node
        return False, None

if __name__ == "__main__":
    print("--- 场景1: 正常 DAG ---")
    dg = DependencyGraph()
    dg.add_subgoal("g1", "query_db")
    dg.add_subgoal("g2", "analyze", depends_on=["g1"])
    dg.add_subgoal("g3", "report", depends_on=["g1", "g2"])
    print(f"  初始可执行: {dg.get_ready()}")
    dg.mark_done("g1")
    print(f"  g1完成后可执行: {dg.get_ready()}")
    print(f"  循环检测: {dg.detect_cycle()}")

    print("\n--- 场景2: 含环 ---")
    dg2 = DependencyGraph()
    dg2.add_subgoal("a", "act_a", depends_on=["c"])
    dg2.add_subgoal("b", "act_b", depends_on=["a"])
    dg2.add_subgoal("c", "act_c", depends_on=["b"])
    print(f"  循环检测: {dg2.detect_cycle()}")
