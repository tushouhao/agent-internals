# 语义漂移检测器
# 运行: python semantic_drift_detector.py

class SemanticDriftDetector:
    """语义漂移检测器：基于工具调用历史的异常检测"""
    def __init__(self, tool_schemas):
        self.tools = tool_schemas
        self.history = []
        # 模拟工具嵌入向量（简化：用工具名哈希到固定向量）
        self.tool_embeddings = {
            name: self._embed(spec.get("description", name))
            for name, spec in tool_schemas.items()
        }
        self.low_frequency_tools = set()  # 长尾工具集合

    def _embed(self, text):
        """简易词嵌入（词频向量，固定维度）"""
        return [len(text) % 7, sum(ord(c) for c in text) % 13]

    def _cosine_distance(self, v1, v2):
        """简化余弦距离"""
        import math
        dot = sum(a*b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a*a for a in v1)) or 1
        n2 = math.sqrt(sum(b*b for b in v2)) or 1
        return 1 - dot / (n1 * n2)

    def _find_semantic_neighbors(self, tool_name):
        """找到与给定工具语义相近的工具"""
        others = [t for t in self.tools if t != tool_name]
        if not others:
            return []
        return sorted(others,
                      key=lambda t: self._cosine_distance(
                          self.tool_embeddings[tool_name],
                          self.tool_embeddings[t]))[:2]

    def detect_drift(self, predicted_tool, user_intent_embedding):
        """检测当前工具选择是否存在语义漂移"""
        if predicted_tool not in self.tools:
            return {"drift": True, "reason": "unknown_tool"}
        if predicted_tool in self.low_frequency_tools:
            similar_tools = self._find_semantic_neighbors(predicted_tool)
            intent_distances = [
                self._cosine_distance(user_intent_embedding,
                                      self.tool_embeddings[t])
                for t in similar_tools
            ]
            if intent_distances:
                min_dist = min(intent_distances)
                if min_dist < 0.3:
                    return {"drift": True,
                            "suggested": similar_tools[intent_distances.index(min_dist)]}
        return {"drift": False}

if __name__ == "__main__":
    schemas = {
        "search_docs": {"description": "搜索文档库", "params": {"q": "string"}},
        "search_web":  {"description": "搜索互联网", "params": {"q": "string"}},
        "send_email":  {"description": "发送邮件", "params": {"to": "string"}},
    }
    detector = SemanticDriftDetector(schemas)
    detector.low_frequency_tools.add("search_web")  # 标记为长尾

    intent = [3, 9]  # 用户意图嵌入
    for tool in ["search_docs", "search_web", "send_email", "unknown_tool"]:
        drift = detector.detect_drift(tool, intent)
        print(f"工具={tool}: {drift}")
