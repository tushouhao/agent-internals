# bfs_dfs_search
# 运行: python bfs_dfs_search.py

def bfs_search(root, max_depth, get_children, is_goal):
    """宽度优先搜索"""
    queue = [(root, 0)]
    visited = set()
    while queue:
        node, depth = queue.pop(0)
        if depth > max_depth:
            continue
        if is_goal(node):
            return node
        visited.add(node)
        for child in get_children(node):
            if child not in visited:
                queue.append((child, depth + 1))
    return None

def dfs_search(node, depth, max_depth, get_children, is_goal):
    """深度优先搜索（递归实现）"""
    if depth > max_depth:
        return None
    if is_goal(node):
        return node
    for child in get_children(node):
        result = dfs_search(child, depth + 1, max_depth,
                            get_children, is_goal)
        if result:
            return result
    return None

if __name__ == "__main__":
    tree = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []}
    children = lambda n: tree.get(n, [])
    is_goal = lambda n: n == "E"
    print(f"BFS: {bfs_search('A', 3, children, is_goal)}")
    print(f"DFS: {dfs_search('A', 0, 3, children, is_goal)}")
