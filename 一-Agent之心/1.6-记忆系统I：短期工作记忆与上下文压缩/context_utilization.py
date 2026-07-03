# context_utilization
# 运行: python context_utilization.py

def measure_context_utilization(messages, window_size):
    """测量上下文利用率与信息损耗"""
    total = sum(estimate_tokens(m["content"]) for m in messages)
    utilization = total / window_size
    # U 型位置衰减: 首尾高, 中段低
    weights = []
    n = len(messages)
    for i in range(n):
        rel = i / max(n - 1, 1)
        w = 1.0 - 0.6 * (1 - 4 * (rel - 0.5) ** 2)
        weights.append(w)
    effective = sum(estimate_tokens(m["content"]) * w
                    for m, w in zip(messages, weights))
    return {"total_tokens": total, "utilization": utilization,
            "effective_tokens": effective,
            "loss_rate": 1 - effective / total}

def estimate_tokens(text):
    """粗略估算 token 数"""
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    en = len(text.split()) - cn // 2
    return int(cn * 1.6 + en * 1.3)

if __name__ == "__main__":
    msgs = [{"role":"system","content":"你是助手"},
            {"role":"user","content":"查订单 OD2024001 物流状态"},
            {"role":"assistant","content":"正在查询..."},
            {"role":"tool","content":"已到达北京分拣中心"},
            {"role":"user","content":"预计什么时候到?"}]
    r = measure_context_utilization(msgs, 32000)
    print(f"上下文统计:")
    for k, v in r.items():
        print(f"  {k}: {v}")

