# agent_kernel_dataflow
# 运行: python agent_kernel_dataflow.py

class AgentKernelDataflow:
    """Agent 内核数据流描述"""
    def __init__(self):
        self.stages = [
            {"name": "输入校验", "article": "1.16", "latency_ms": 20,
             "role": "拦截注入攻击与非法输入"},
            {"name": "提示组装", "article": "1.14", "latency_ms": 10,
             "role": "选取少样本示例 + 拼装提示模板"},
            {"name": "LLM 推理", "article": "1.2", "latency_ms": 800,
             "role": "核心推理引擎, 占总延迟 62%"},
            {"name": "推理增强", "article": "1.9-1.13", "latency_ms": 3200,
             "role": "CoT/ToT/反思/自一致性, 按需启用"},
            {"name": "工具调用", "article": "1.3", "latency_ms": 200,
             "role": "调用外部工具扩展能力边界"},
            {"name": "规划执行", "article": "1.4-1.5", "latency_ms": 150,
             "role": "多步任务的子目标分解与执行"},
            {"name": "动作审计", "article": "1.16", "latency_ms": 50,
             "role": "检测异常动作模式"},
            {"name": "人工审批", "article": "1.16", "latency_ms": 900000,
             "role": "高危动作的人工确认 (15min)"},
            {"name": "执行+观察", "article": "1.1", "latency_ms": 300,
             "role": "执行动作并观察环境反馈"},
            {"name": "记忆更新", "article": "1.6-1.8", "latency_ms": 40,
             "role": "将本次经验写入短期/长期/向量记忆"},
            {"name": "评估记录", "article": "1.15", "latency_ms": 30,
             "role": "四维评估并写入审计日志"},
        ]

    def critical_path(self):
        """关键路径: 无人工审批时的总延迟"""
        auto_stages = [s for s in self.stages if "审批" not in s["name"]]
        total = sum(s["latency_ms"] for s in auto_stages)
        return {"total_ms": total, "bottleneck": "LLM 推理",
                "bottleneck_pct": 800 / total * 100}

    def memory_flow(self):
        """记忆数据流"""
        return {
            "short_term": "1.6 上下文窗口, 当前对话",
            "long_term": "1.7 跨会话摘要 + 结构化笔记",
            "vector": "1.8 向量检索, 语义相似记忆",
            "coordination": "三层协作: 短期实时 + 长期摘要 + 向量检索 top-k",
        }
if __name__ == "__main__":
    df = AgentKernelDataflow()
    cp = df.critical_path()
    print(f"关键路径总延迟: {cp['total_ms']}ms")
    print(f"瓶颈: {cp['bottleneck']} ({cp['bottleneck_pct']:.0f}%)")
    mf = df.memory_flow()
    print(f"\n记忆数据流:")
    for k, v in mf.items():
        print(f"  {k}: {v}")

