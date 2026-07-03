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
