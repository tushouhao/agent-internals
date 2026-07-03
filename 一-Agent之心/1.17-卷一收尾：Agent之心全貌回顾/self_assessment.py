# self_assessment
# 运行: python self_assessment.py

class SelfAssessment:
    """卷一知识自测"""
    def __init__(self):
        self.questions = [
            {"q": "ReAct 循环的四个阶段是?", "a": "Thought-Action-Observation-Loop",
             "related": "1.1"},
            {"q": "工具调用描述中结构化四要素是?", "a": "名称+参数+返回+示例", "related": "1.3"},
            {"q": "上下文窗口利用率的安全阈值是?", "a": "70%, 超过后准确率降 9.4 个百分点", "related": "1.6"},
            {"q": "ToT 在 24 点游戏上的准确率与 CoT 对比?", "a": "74.0% vs 20.8%, 但成本 12.8 倍", "related": "1.11"},
            {"q": "修正悖论的核心发现是?", "a": "无外部信号时自我修正降 4.3 个百分点", "related": "1.12"},
            {"q": "自一致性的性价比拐点 N 是?", "a": "N=10, 1倍成本换 +13.3 个百分点", "related": "1.13"},
            {"q": "示例选取最优策略是?", "a": "相似度检索, 比随机 +8.7 且方差降 5 倍", "related": "1.14"},
            {"q": "Agent 四维评估是哪四维?", "a": "结果/过程/效率/成本", "related": "1.15"},
            {"q": "四层安全防御将危险动作率从多少降至多少?", "a": "4.7% 降至 0.12%", "related": "1.16"},
            {"q": "卷一与卷二的衔接逻辑是?", "a": "原理地图是框架选型的判断依据", "related": "1.17"},
        ]

    def quiz(self):
        """自测: 返回问题, 读者自答后核对"""
        return [{"question": q["q"], "related": q["related"]} for q in self.questions]

    def grade(self, answers):
        """评分: answers 是读者答案列表"""
        correct = 0
        for i, ans in enumerate(answers):
            if self._fuzzy_match(ans, self.questions[i]["a"]):
                correct += 1
        return {"score": correct, "total": len(self.questions),
                "level": self._level(correct / len(self.questions))}

    def _fuzzy_match(self, ans, expected):
        key_terms = [w for w in expected.split() if len(w) > 2]
        return sum(1 for t in key_terms if t in ans) >= len(key_terms) * 0.5

    def _level(self, ratio):
        if ratio >= 0.9: return "A: 可进入卷二"
        if ratio >= 0.7: return "B: 建议复习薄弱章节"
        if ratio >= 0.5: return "C: 需重读卷一"
        return "D: 建议从 1.1 重新开始"
if __name__ == "__main__":
    test = SelfAssessment()
    quiz = test.quiz()
    print(f"共 {len(quiz)} 道自测题:\n")
    for i, q in enumerate(quiz, 1):
        print(f"{i}. [{q['related']}] {q['question']}")
    # 模拟作答评分
    sample_answers = [
        "Thought Action Observation Loop",
        "名称 参数 返回 示例",
        "70%",
        "74% vs 20%",
        "无信号降4.3%",
        "N=10",
        "相似度检索",
        "结果 过程 效率 成本",
        "4.7% 降至 0.12%",
        "原理是选型依据",
    ]
    grade = test.grade(sample_answers)
    print(f"\n模拟评分: {grade['score']}/{grade['total']} -> {grade['level']}")

