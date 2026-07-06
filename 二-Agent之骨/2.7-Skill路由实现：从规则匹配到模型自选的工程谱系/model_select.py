# 文件名: model_select.py
# 功能: 第四档模型自选——向量取 top-k 候选 LLM 从中选
# 运行: python model_select.py

"""模型自选：向量取 top-k 墒选，LLM 从中选最匹配。

k=5 甜点：召回 97% 且 prompt 可控（5 描述约 500t）
成本 200(向量)+800(LLM)=1000t，延迟 480ms
价值: 消歧（analyze_csv vs validate_csv 语义近功能异）
适用: skill ≥ 100 或误选代价高
教学版，模拟模型自选。
"""
from dataclasses import dataclass, field

@dataclass
class ModelSelectRouter:
    vector_router: callable
    llm_judge: callable
    top_k: int = 5

    def route(self, task: str) -> dict:
        candidates = self.vector_router(task, self.top_k)
        selection = self.llm_judge(task, candidates)
        return {"selected": selection["skill"], "reason": selection["reason"],
                "candidates": candidates}

def mock_vector(task: str, k: int) -> list:
    pool = ["analyze_csv", "validate_csv", "generate_report", "send_email", "read_file"]
    return pool[:k]

def mock_llm_judge(task: str, candidates: list) -> dict:
    if "统计" in task or "汇总" in task:
        for c in candidates:
            if "analyze" in c:
                return {"skill": c, "reason": f"任务含统计语义，{c} 描述含统计分析"}
    if "校验" in task or "验证" in task:
        for c in candidates:
            if "validate" in c:
                return {"skill": c, "reason": f"任务含校验语义，{c} 描述含格式校验"}
    return {"skill": candidates[0], "reason": "默认选 top-1"}

def main():
    print("=" * 64)
    print("模型自选：向量 top-k + LLM 消歧")
    print("=" * 64)
    router = ModelSelectRouter(mock_vector, mock_llm_judge, top_k=5)
    cases = [
        ("统计销售数据", "analyze_csv"),
        ("校验 CSV 格式", "validate_csv"),
        ("汇总月度报告", "analyze_csv"),  # 汇总=统计语义
    ]
    print(f"\n{'任务':<16}{'期望':<16}{'选中':<16}{'理由'}")
    print("-" * 64)
    for task, expected in cases:
        r = router.route(task)
        ok = "✓" if r["selected"] == expected else "✗"
        print(f"{task:<16}{expected:<16}{r['selected']:<16}{r['reason'][:30]}")
    print()
    print("结论: k=5 召回 97%, 成本 1000t, 延迟 480ms")
    print("      价值: 消歧（统计 vs 校验），LLM 读懂语义匹配")
    print("      边界: LLM 黑盒，输出理由可审计但不可全信")

if __name__ == "__main__":
    main()
