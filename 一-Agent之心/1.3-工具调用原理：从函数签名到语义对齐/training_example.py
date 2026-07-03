# Function Calling 训练数据格式
# 运行: python training_example.py

# 工具调用训练数据的标准格式
training_example = {
    "messages": [
        {"role": "system", "content": "你是一个客服助手，可以使用以下工具..."},
        {"role": "user", "content": "帮我查一下订单 OD2024001 的物流状态"},
        {"role": "assistant", "content": None,
         "tool_calls": [
             {"id": "call_001",
              "type": "function",
              "function": {
                  "name": "query_logistics",
                  "arguments": '{"order_id": "OD2024001"}'
              }}
         ]},
        {"role": "tool", "content": "包裹已到达北京分拣中心",
         "tool_call_id": "call_001"}
    ]
}

if __name__ == "__main__":
    print("=== Function Calling 训练样本 ===")
    for msg in training_example["messages"]:
        role = msg["role"]
        content = msg.get("content", "")
        if msg.get("tool_calls"):
            tc = msg["tool_calls"][0]
            print(f"  [{role}] 调用工具: {tc['function']['name']}({tc['function']['arguments']})")
        else:
            print(f"  [{role}] {content or '(空)'}")
