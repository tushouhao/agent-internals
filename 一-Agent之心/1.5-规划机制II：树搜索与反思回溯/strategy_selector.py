# strategy_selector
# 运行: python strategy_selector.py

class SearchStrategySelector:
    """搜索策略选择器"""
    def select(self, task):
        bf = task.get("branching_factor", 3)
        dp = task.get("depth", 6)
        rd = task.get("reward_density", 0.1)
        time_budget = task.get("time_budget_ms", 5000)

        complexity = bf ** dp

        # 极深或极宽的搜索空间
        if complexity > 10000 or bf > 6:
            return "MCTS" if time_budget > 10000 else "reflection"

        # 中等复杂度
        if bf < 4 and dp < 8:
            if rd > 0.3:
                return "dfs"      # 高奖励密度，DFS 足够
            return "mcts"         # 低奖励密度需要导向

        # 深度优先 vs 宽度优先
        if bf <= dp:
            return "dfs"          # 深度大的空间
        return "bfs"              # 宽度大的空间
