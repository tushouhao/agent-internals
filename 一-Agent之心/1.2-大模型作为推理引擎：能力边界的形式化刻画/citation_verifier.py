# 引文验证器
# 运行: python citation_verifier.py

# 引文辅助函数：从文本中提取形如 Word2020 的引用
import re

def extract_citations(text):
    """从文本中提取引用（形如 Name2020 的模式）"""
    pattern = r'\b([A-Z][a-z]+\d{4})\b'
    return [{"doi": m, "raw": m} for m in re.findall(pattern, text)]

# 引文验证器：将 LLM 生成的引用与知识库交叉验证
def verify_citations(text, known_database):
    citations = extract_citations(text)
    valid, invalid = 0, 0
    for cite in citations:
        if cite["doi"] in known_database:
            valid += 1
        else:
            invalid += 1
    total = len(citations)
    rate = invalid / total if total > 0 else 0.0
    return {"valid": valid, "invalid": invalid, "total": total, "hallucination_rate": rate}

if __name__ == "__main__":
    db = {"Smith2020", "Lee2021", "Wang2022"}
    text = "根据 Smith2020 的研究，效率提升 30%。Johnson2023 也证实了这一点。"
    result = verify_citations(text, db)
    print(f"引用验证结果: {result}")
    print(f"命中: {result['valid']}, 缺失: {result['invalid']}, 幻觉率: {result['hallucination_rate']*100:.0f}%")
