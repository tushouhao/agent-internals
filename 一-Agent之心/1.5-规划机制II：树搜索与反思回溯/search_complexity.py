# search_complexity
# 运行: python search_complexity.py

def estimate_search_complexity(depth, branching_factor):
    """估算搜索复杂度"""
    return branching_factor ** depth

def estimate_success_rate(search_paths, reward_density):
    """预估搜索成功率"""
    return 1 - (1 - reward_density) ** search_paths

if __name__ == "__main__":
    for d in [4, 6, 8]:
        for b in [2, 3, 5]:
            c = estimate_search_complexity(d, b)
            print(f"深度{d} 分支{b}: 复杂度={c}")
    print("\n成功率预估 (1000 路径):")
    for rd in [0.05, 0.15, 0.30]:
        print(f"  奖励密度{rd}: {estimate_success_rate(1000, rd)*100:.1f}%")
