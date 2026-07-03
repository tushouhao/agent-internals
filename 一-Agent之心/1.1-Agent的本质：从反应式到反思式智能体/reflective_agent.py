# 反思式 Agent：自评 + 修正循环
# 运行: python reflective_agent.py


def reflective_agent(task: str, llm, verifier, max_rounds: int = 3) -> str:
    """反思式 Agent：执行 - 评分 - 修正"""
    output = llm(task)
    for round_idx in range(max_rounds):
        score = verifier(task, output)
        if score >= 0.85:
            return output
        feedback = f"评分{score:.2f}，需要修正"
        output = llm(f"原始问题: {task}\n当前输出: {output}\n{feedback}")
    return output


if __name__ == "__main__":
    # 模拟 LLM
    def mock_llm(prompt: str) -> str:
        if "修正" in prompt:
            return "修正后的答案: 42"
        return "初步答案: 43"

    # 模拟验证器
    def mock_verifier(task: str, output: str) -> float:
        if "42" in output:
            return 0.95
        return 0.60

    result = reflective_agent("6 * 7 = ?", mock_llm, mock_verifier, max_rounds=3)
    print(f"反思式结果: {result}")

    # 验证：如果 LLM 初始输出为 43（错误），经过一轮修正后应为 42
    assert "42" in result, f"预期包含42，实际: {result}"
    print("反思式 Agent 测试通过")
