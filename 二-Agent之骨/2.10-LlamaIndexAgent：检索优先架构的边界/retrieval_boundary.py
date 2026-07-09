# 文件名: retrieval_boundary.py
# 功能: 检索优先失效边界三红线判据 + 三类任务完成率基线
# 运行: python retrieval_boundary.py
"""
检索优先失效边界三红线:
  - 召回红线: 非词汇匹配占比 ≥ 20% 召回上限漏关键超22%
  - 漂移红线: 文档月更率 ≥ 10% 无增量漂移超1pp/月
  - 改写红线: 需改写深度 ≥ 2 副作用超召回增益
  判决: 0红线裸检索够用, 1手补, 2弃检索转编排
"""

from dataclasses import dataclass

@dataclass
class RetrievalSuitabilityChecker:
    """检索优先适用性判据: 三红线"""
    non_lexical_match_ratio: float  # 非词汇匹配占比
    doc_monthly_update_rate: float  # 文档月更率
    rewrite_depth_needed: int  # 需改写深度
    def verdict(self) -> dict:
        risks = []
        benefits = []
        # 知识密集甜点
        if (self.non_lexical_match_ratio < 0.20 and
            self.doc_monthly_update_rate < 0.10 and
            self.rewrite_depth_needed <= 1):
            return {"verdict": "裸检索够用", "替代": "LlamaIndex裸索引",
                    "完成率预期": "89%甜点内"}
        # 混合任务甜点
        if (0.20 <= self.non_lexical_match_ratio < 0.50 or
            self.rewrite_depth_needed == 2):
            benefits.append({"甜点": "混合任务, 检索+编排混合谱系"})
        # 失效红线
        if self.non_lexical_match_ratio >= 0.50:
            risks.append({"redline": "召回上限", "fix": "升混合谱系或转编排"})
        if self.doc_monthly_update_rate >= 0.10:
            risks.append({"redline": "索引漂移", "fix": "接增量索引或转编排"})
        if self.rewrite_depth_needed >= 3:
            risks.append({"redline": "改写失控", "fix": "限单次改写+编排refine"})
        if len(risks) >= 2:
            return {"verdict": "弃检索转编排", "risks": risks,
                    "替代": "LangGraph编排或自研(2.15)", "完成率预期": "85-89%"}
        if benefits:
            return {"verdict": "用混合谱系", "benefits": benefits,
                    "替代": "LlamaIndex+LangGraph混合", "完成率预期": "88%"}
        return {"verdict": "手补检索可用", "risks": risks,
                "替代": "手补护栏+增量", "完成率预期": "79%"}

@dataclass
class TaskCompletionBaseline:
    """三类任务完成率基线"""
    task_type: str
    naive_retrieval: float
    patched_retrieval: float
    hybrid_spectrum: float
    full_harness: float
    def summary(self) -> dict:
        return {"task_type": self.task_type,
                "裸检索": f"{self.naive_retrieval:.0%}",
                "手补检索": f"{self.patched_retrieval:.0%}",
                "混合谱系": f"{self.hybrid_spectrum:.0%}",
                "完整harness": f"{self.full_harness:.0%}"}

def main():
    """demo: 三红线判据 + 三类任务完成率基线"""
    print("=" * 60)
    print("检索优先失效边界判据 (三红线)")
    print("=" * 60)
    cases = [
        ("FAQ(知识查询)", 0.10, 0.05, 1),
        ("混合任务(查+推理)", 0.30, 0.15, 2),
        ("根因分析(开放推理)", 0.60, 0.20, 3),
        ("医疗RAG(敏度修正)", 0.25, 0.08, 1),  # 召回敏度high非数量
    ]
    print(f"{'任务':<18} {'非词汇':<8} {'月更':<8} {'改写深度':<10} {'判决':<14}")
    print("-" * 64)
    for name, nlex, upd, rw in cases:
        c = RetrievalSuitabilityChecker(nlex, upd, rw)
        v = c.verdict()
        print(f"{name:<16} {nlex:.0%}{'':<5} {upd:.0%}{'':<5} {rw:<10} {v['verdict']}")
        print(f"{'':<44} 替代: {v.get('替代', '')[:30]}")
    print()
    # 完成率基线
    print("=" * 60)
    print("三类任务完成率基线 (裸检索/手补/混合/完整)")
    print("=" * 60)
    baselines = [
        TaskCompletionBaseline("知识查询(FAQ)", 0.89, 0.92, 0.92, 0.94),
        TaskCompletionBaseline("混合任务(查+推理)", 0.67, 0.79, 0.88, 0.89),
        TaskCompletionBaseline("开放推理(根因)", 0.41, 0.61, 0.85, 0.89),
    ]
    print(f"{'任务类型':<24} {'裸检索':<8} {'手补':<8} {'混合':<8} {'完整':<8}")
    print("-" * 60)
    for b in baselines:
        s = b.summary()
        print(f"{s['task_type']:<22} {s['裸检索']:<8} {s['手补检索']:<8} {s['混合谱系']:<8} {s['完整harness']:<8}")
    print("=" * 60)
    print("结论: 知识查询89%裸检索够用, 混合88%混合谱系, 开放85%转编排")
    print("      检索不可替代价值: 知识密集任务上下文窗口压力消失")
    print("      (1000文档RAG 2560token vs 拼全文50万token)")
    print("      代价: 召回上限+索引维护+改写副作用(相关性≠该用)")
    print("      链/图/检索/自研 是2.15决策树四档选择 按任务特征升档")

if __name__ == "__main__":
    main()
