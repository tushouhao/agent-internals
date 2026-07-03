# alignment_paradigms
# 运行: python alignment_paradigms.py

class AlignmentParadigms:
    """三种对齐范式对比"""
    def __init__(self, paradigm="rules"):
        self.paradigm = paradigm
        if paradigm == "rules":
            self.rules = [
                "禁止输出个人身份信息",
                "禁止提供违法建议",
                "拒绝执行删除操作未经确认",
                "不讨论政治敏感话题",
            ]
        elif paradigm == "constitutional":
            self.constitution = [
                "不造成伤害",
                "尊重用户自主权",
                "诚实不欺骗",
                "遵守法律",
            ]
        # RLHF 需训练, 这里仅模拟
    def align(self, response, context):
        """对齐检查"""
        if self.paradigm == "rules":
            return self._rule_check(response)
        elif self.paradigm == "constitutional":
            return self._constitutional_check(response, context)
        elif self.paradigm == "rlhf":
            return {"aligned": True, "paradigm": "rlhf (模型内置)"}
        return {"aligned": True}
    def _rule_check(self, response):
        for rule in self.rules:
            keywords = self._rule_keywords(rule)
            for kw in keywords:
                if kw in response:
                    return {"aligned": False, "violated": rule, "keyword": kw}
        return {"aligned": True}
    def _constitutional_check(self, response, context):
        """基于宪法的自我审查"""
        for principle in self.constitution:
            if self._violates_principle(response, principle):
                return {"aligned": False, "violated": principle}
        return {"aligned": True}
    def _rule_keywords(self, rule):
        if "个人信息" in rule: return ["身份证", "手机号", "地址", "社保号"]
        if "违法" in rule: return ["毒品", "黑客", "伪造", "逃税"]
        if "删除" in rule: return ["DELETE", "drop table", "rm -rf"]
        if "政治" in rule: return ["政治", "选举", "政党"]
        return []
    def _violates_principle(self, response, principle):
        if "伤害" in principle:
            return any(w in response for w in ["伤害", "攻击", "毒害"])
        if "诚实" in principle:
            return "我不知道" in response and "其实知道" in response
        return False
if __name__ == "__main__":
    for paradigm in ["rules", "constitutional"]:
        aligner = AlignmentParadigms(paradigm)
        tests = [
            ("这是身份证号 110101199001011234", "个人信息"),
            ("可以尝试伪造文件", "违法"),
            ("正常回答没问题", "正常"),
        ]
        print(f"\n{paradigm} 范式:")
        for resp, desc in tests:
            r = aligner.align(resp, {})
            status = "✗违规" if not r["aligned"] else "✓合规"
            print(f"  {status} {desc}: {r}")

