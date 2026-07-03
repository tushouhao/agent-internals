# 语义漂移检测器
# 运行: python semantic_drift_detector.py

class SemanticDriftDetector:
    """语义漂移检测器：基于工具调用历史的异常检测"""
    def __init__(self, tool_schemas):
        self.tools = tool_schemas
        self.history = []

    def detect_drift(self, predicted_tool, user_intent_embedding):
        """检测当前工具选择是否存在语义漂移"""
        # 1. 检查是否是长尾工具
        if predicted_tool in self.low_frequency_tools:
            # 2. 与相似工具的语义距离对比
            similar_tools = self._find_semantic_neighbors(predicted_tool)
            intent_distances = [
                self._cosine_distance(user_intent_embedding,
                                      self.tool_embeddings[t])
                for t in similar_tools
            ]
            min_dist = min(intent_distances)
            if min_dist < 0.3:
                return {"drift": True,
                        "suggested": similar_tools[intent_distances.index(min_dist)]}
        return {"drift": False}
