# volume1_map
# 运行: python volume1_map.py

class Volume1Map:
    """卷一 17 篇主题群映射"""
    def __init__(self):
        self.clusters = {
            "本质": {"articles": ["1.1 Agent 的灵魂", "1.2 大模型作为推理引擎"],
                     "core_question": "Agent 是什么? LLM 如何作为推理核心?",
                     "key_metric": "ReAct 循环延迟 800ms, 推理占延迟 62%"},
            "推理基础": {"articles": ["1.3 工具调用原理", "1.4 规划机制 I", "1.5 规划机制 II"],
                         "core_question": "Agent 如何调用工具? 如何规划多步任务?",
                         "key_metric": "工具调用成功率 91.2%, 规划深度 5 步后准确率降 28%"},
            "记忆": {"articles": ["1.6 记忆系统 I", "1.7 记忆系统 II", "1.8 记忆系统 III"],
                     "core_question": "Agent 如何记住上下文? 短期/长期/向量记忆如何协作?",
                     "key_metric": "上下文窗口利用率超 70% 后准确率降 9.4 个百分点"},
            "推理引擎": {"articles": ["1.9-1.14 六篇推理引擎系列"],
                        "core_question": "CoT/ToT/反思/自一致性/提示工程如何提升推理质量?",
                        "key_metric": "ToT 74.0% vs CoT 20.8% (24点), 但成本 12.8 倍"},
            "评估": {"articles": ["1.15 Agent 评估与基准测试"],
                     "core_question": "如何量化 Agent 能力边界?",
                     "key_metric": "四维评估结果-过程相关系数仅 r=0.54"},
            "安全": {"articles": ["1.16 Agent 安全性与对齐"],
                     "core_question": "如何防止 Agent 造成不可逆损害?",
                     "key_metric": "四层防御将危险动作率从 4.7% 降至 0.12%"},
        }

    def navigate(self, question):
        """根据问题导航到主题群"""
        keywords = {
            "本质": ["是什么", "定义", "核心", "LLM"],
            "推理基础": ["工具", "调用", "规划", "多步"],
            "记忆": ["记忆", "上下文", "向量", "长期"],
            "推理引擎": ["CoT", "ToT", "反思", "自一致性", "提示"],
            "评估": ["评估", "基准", "测试", "度量"],
            "安全": ["安全", "对齐", "注入", "防御"],
        }
        for cluster, kws in keywords.items():
            if any(kw in question for kw in kws):
                return self.clusters[cluster]
        return None

    def stats(self):
        """卷一统计"""
        return {"articles": 17, "lines": 6300, "mermaid": 104,
                "python_files": 104, "data_points": 52, "verified": "17/17"}
if __name__ == "__main__":
    m = Volume1Map()
    # 按问题导航
    for q in ["Agent 是什么?", "如何调用工具?", "记忆怎么存?", "ToT 是什么?", "怎么评估?"]:
        r = m.navigate(q)
        print(f"Q: {q} -> {r['articles'][0] if r else '无'}")
    print(f"\n卷一统计: {m.stats()}")

