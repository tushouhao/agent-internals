# search_complexity
# 运行: python search_complexity.py

def estimate_search_complexity(depth, branching_factor):
    """估算搜索复杂度"""
    return branching_factor ** depth

def estimate_success_rate(search_paths, reward_density):
    """预估搜索成功率"""
    return 1 - (1 - reward_density) ** search_paths
