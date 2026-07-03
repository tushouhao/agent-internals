# 引文验证器
# 运行: python citation_verifier.py

# 引文验证器：将 LLM 生成的引用与知识库交叉验证
def verify_citations(text, known_database):
    citations = extract_citations(text)
    valid, invalid = 0, 0
    for cite in citations:
        if cite["doi"] in known_database:
            valid += 1
        else:
            invalid += 1
    return {"valid": valid, "total": len(citations), "hallucination_rate": invalid / len(citations)}
