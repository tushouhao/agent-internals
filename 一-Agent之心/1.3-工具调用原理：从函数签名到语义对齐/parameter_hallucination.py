# 参数幻觉示例
# 运行: python parameter_hallucination.py

# 参数幻觉的三种典型表现
parameter_hallucination_examples = [
    {
        "type": "不存在参数",
        "input": "帮我查一下北京的天气",
        "tool": "get_weather",
        "expected": '{"city": "Beijing"}',
        "actual": '{"city": "Beijing", "unit": "celsius", "language": "zh"}',
        # "unit" 和 "language" 不是 get_weather 的参数
        "error": "额外参数被 schema 校验拒绝"
    },
    {
        "type": "参数值格式错误",
        "input": "查订单 12345",
        "tool": "query_order",
        "expected": '{"order_id": "12345"}',
        "actual": '{"order_id": 12345}',
        # order_id 要求 string 类型，模型传了 int
        "error": "类型校验失败"
    },
]

if __name__ == "__main__":
    print(f"参数幻觉示例 {len(parameter_hallucination_examples)} 例:")
    for ex in parameter_hallucination_examples:
        print(f"  [{ex['type']}] {ex['input']}")
        print(f"    预期: {ex['expected']}")
        print(f"    实际: {ex['actual']}")
        print(f"    错误: {ex['error']}")
