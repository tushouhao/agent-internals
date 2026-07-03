# tree_of_thoughts
# 运行: python tree_of_thoughts.py

def tree_of_thoughts(problem, max_depth=3, branches_per_level=3):
    """树状思维：LLM 评估每个分支"""
    root = {"state": problem, "value": 1.0}

    def evaluate_branch(prefix, candidate):
        """让 LLM 评估候选分支的价值"""
        prompt = f"问题: {problem}\n当前路径: {prefix}\n候选: {candidate}\n该候选方案有多大概率成功？给出 0-1 分。"
        score = float(llm_evaluate(prompt))
        return score

    best_path = [root]
    for depth in range(max_depth):
        current = best_path[-1]["state"]
        # 生成候选分支
        candidates = llm_generate_branches(current, branches_per_level)
        # 评估每个分支
        scored = []
        for cand in candidates:
            score = evaluate_branch(current, cand)
            scored.append((cand, score))
        # 选择最优分支
        scored.sort(key=lambda x: -x[1])
        best_path.append({"state": scored[0][0], "value": scored[0][1]})

    return best_path
