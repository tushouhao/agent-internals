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

    def get_ready(self):
        """返回所有前置依赖已完成的子目标"""
        ready = []
        for name, deps in self.edges.items():
            if self.nodes[name]["status"] == "pending":
                if all(self.nodes[d]["status"] == "done" for d in deps):
                    ready.append(name)
        return ready

    def detect_cycle(self):
        """检测环：使用拓扑排序"""
        visited = set()
        path = set()

        def dfs(node):
            if node in path:
                return True  # 发现环
            if node in visited:
                return False
            visited.add(node)
            path.add(node)
            # 遍历所有依赖当前节点的子目标
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
