# NLU 边缘场景评估
# 运行: python nlu_evaluator.py

from types import SimpleNamespace

def evaluate_nlu_edge_cases(llm, test_suite):
    """评估 LLM 在 NLU 边缘场景的表现"""
    results = {}
    for case in test_suite:
        # 否定嵌套测试
        if "double_negation" in case.tags:
            pred = llm(case.input)
            results["double_negation"] = {
                "correct": pred == case.expected,
                "input": case.input,
                "expected": case.expected,
                "pred": pred,
            }
        # 隐含前提测试
        if "implicit_premise" in case.tags:
            pred = llm(case.input)
            results["implicit_premise"] = {
                "correct": pred == case.expected,
                "input": case.input,
                "expected": case.expected,
                "pred": pred,
            }
    return results

if __name__ == "__main__":
    def mock_llm(prompt):
        if "并非不" in prompt:
            return "是"
        if "首都" in prompt:
            return "北京"
        return "未知"

    suite = [
        SimpleNamespace(input="这件事并非不正确", expected="是",
                        tags=["double_negation"]),
        SimpleNamespace(input="中国的首都是哪里？", expected="北京",
                        tags=["implicit_premise"]),
    ]
    result = evaluate_nlu_edge_cases(mock_llm, suite)
    print(f"NLU 边界测试结果:")
    for k, v in result.items():
        print(f"  [{k}] 正确={v['correct']} 输入='{v['input']}' 预期='{v['expected']}' 预测='{v['pred']}'")
