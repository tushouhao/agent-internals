# volume_bridge
# 运行: python volume_bridge.py

class VolumeBridge:
    """卷一原理到卷二框架的映射"""
    def __init__(self):
        self.bridge = {
            "1.1 Agent 灵魂 (ReAct 循环)": "LangGraph 的 StateGraph / CrewAI 的 Agent 循环",
            "1.2 LLM 推理引擎": "LiteLLM 统一接口 / OpenAI SDK",
            "1.3 工具调用": "LangChain Tool / CrewAI Tool / OpenAI Function Calling",
            "1.4-1.5 规划机制": "LangGraph 的 Plan-Execute / AutoGPT Planner",
            "1.6-1.8 记忆系统": "LangChain Memory / Mem0 / 向量库 (Chroma/Pinecone)",
            "1.9-1.10 CoT 与推理链": "LangChain 的 LLMChain + 自定义 prompt",
            "1.11 ToT": "LangGraph 的 Tree of Thoughts 实现 / langchain.experimental.tot",
            "1.12 反思机制": "LangGraph 的 Reflection 节点 / Reflexion 框架",
            "1.13 自一致性": "LangChain 的 SelfConsistencyChain / 自定义并行采样",
            "1.14 提示工程": "LangSmith 提示管理 / Promptflow / LangChain Hub",
            "1.15 评估": "LangSmith Evaluators / RAGAS / DeepEval",
            "1.16 安全": "Guardrails AI / NeMo Guardrails / LangChain 安全工具",
        }

    def recommend_framework(self, requirement):
        """根据需求推荐框架组件"""
        if "循环" in requirement: return "LangGraph StateGraph"
        if "工具" in requirement: return "LangChain Tool / OpenAI Function Calling"
        if "记忆" in requirement: return "Mem0 + Chroma 向量库"
        if "规划" in requirement: return "LangGraph Plan-Execute"
        if "反思" in requirement: return "LangGraph Reflection 节点"
        if "评估" in requirement: return "LangSmith + RAGAS"
        if "安全" in requirement: return "Guardrails AI"
        return "LangChain (通用)"
if __name__ == "__main__":
    bridge = VolumeBridge()
    print("卷一原理 -> 卷二框架映射:")
    for principle, framework in list(bridge.bridge.items())[:5]:
        print(f"  {principle[:25]}... -> {framework}")
    print(f"\n(共 {len(bridge.bridge)} 个映射)\n")
    # 按需求推荐
    for req in ["循环", "工具", "记忆", "规划", "反思", "评估", "安全"]:
        print(f"需求'{req}' -> {bridge.recommend_framework(req)}")

