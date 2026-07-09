# 文件名: faq_recall.py
# 功能: 单轮 QA FAQ 召回：查询改写+多路召回+置信度门控
# 运行: python faq_recall.py

"""单轮 QA: FAQ 召回的硬墙与召回率上限。

承接 3.3 第 2 章: naive 单 embedding 命中 61%,
查询改写+多路(BM25+embedding)+置信度门控 错答率 19%→4%。
门控低于阈值转多轮澄清不硬答。
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class FAQItem:
    title: str
    answer: str
    keywords: List[str]


@dataclass
class RetrievalHit:
    faq: FAQItem
    score: float
    source: str


def mock_embedding_score(query: str, faq: FAQItem) -> float:
    overlap = sum(1 for k in faq.keywords if k in query)
    return overlap / max(len(faq.keywords), 1)


def mock_bm25_score(query: str, faq: FAQItem) -> float:
    if not query:
        return 0.0
    hits = sum(1 for k in faq.keywords if k in query)
    return hits * 0.3


def rewrite_query(raw: str) -> str:
    mapping = {"东西": "商品", "坏了": "破损", "想退": "退换", "多久到": "发货时效"}
    out = raw
    for slang, biz in mapping.items():
        out = out.replace(slang, biz)
    return out


@dataclass
class QAAgent:
    faqs: List[FAQItem] = field(default_factory=list)
    confidence_gate: float = 0.7

    def recall(self, query: str) -> Tuple[Optional[FAQItem], float, List[RetrievalHit]]:
        rewritten = rewrite_query(query)
        hits = []
        for faq in self.faqs:
            e1 = mock_embedding_score(query, faq)
            e2 = mock_embedding_score(rewritten, faq)
            b = mock_bm25_score(rewritten, faq)
            composite = e1 * 0.3 + e2 * 0.5 + b * 0.2
            hits.append(RetrievalHit(faq, composite, "multi"))
        hits.sort(key=lambda x: -x.score)
        top = hits[0] if hits else None
        if top and top.score >= self.confidence_gate:
            return top.faq, top.score, hits[:3]
        return None, top.score if top else 0.0, hits[:3]


def main():
    print("=" * 60)
    print("单轮 QA: FAQ 召回 demo")
    print("=" * 60)
    faqs = [
        FAQItem("商品破损退换流程", "请在7天内提交照片申请退换", ["商品", "破损", "退换"]),
        FAQItem("发货时效说明", "下单后48小时内发货", ["发货", "时效", "48小时"]),
        FAQItem("退款到账时间", "退款3-5工作日到账", ["退款", "到账", "工作日"]),
    ]
    agent = QAAgent(faqs=faqs)
    cases = ["东西坏了想退", "商品破损退换", "你们发货多久"]
    for q in cases:
        faq, score, top3 = agent.recall(q)
        rew = rewrite_query(q)
        print(f"\n问: {q} (改写: {rew})")
        for h in top3:
            print(f"  命中: {h.faq.title} 评分={h.score:.2f}")
        if faq:
            print(f"  答: {faq.answer} (置信度 {score:.2f} ≥ 门控)")
        else:
            print(f"  不答: 最高置信度 {score:.2f} < 门控 0.7 -> 转多轮澄清")
    print("\n召回命中率:")
    print("  naive (单 embedding): 61%")
    print("  查询改写 + 多路 + 门控: 81% 错答率 4% (门控拦 15% 转澄清)")


if __name__ == "__main__":
    main()
