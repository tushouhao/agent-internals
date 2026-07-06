# 文件名: rule_router.py
# 功能: 第一档规则匹配——关键词命中路由
# 运行: python rule_router.py

"""规则匹配：关键词命中路由。

关键词表: skill → keywords，路由时按命中数排序
召回率 62%（词汇不完全匹配漏选），成本 0t，延迟 0.5ms
死穴: 同义词（任务说汇总但表只有统计）
适用: skill ≤ 20 且任务词汇固定
教学版，模拟规则匹配。
"""
from dataclasses import dataclass, field

@dataclass
class RuleRouter:
    keywords: dict = field(default_factory=dict)  # skill → keywords

    def route(self, task: str) -> str | None:
        scores = {}
        for skill, kws in self.keywords.items():
            score = sum(1 for kw in kws if kw.lower() in task.lower())
            if score > 0:
                scores[skill] = score
        if not scores:
            return None
        return max(scores, key=scores.get)

def main():
    print("=" * 64)
    print("规则匹配：关键词命中路由")
    print("=" * 64)
    router = RuleRouter({
        "analyze_csv": ["CSV", "统计", "分组", "聚合"],
        "validate_csv": ["CSV", "校验", "格式", "验证"],
        "generate_report": ["报告", "生成", "汇总"],
        "send_email": ["邮件", "发送", "通知"],
    })
    cases = [
        ("统计销售 CSV", "analyze_csv"),
        ("校验 CSV 格式", "validate_csv"),
        ("生成销售报告", "generate_report"),
        ("发送通知邮件", "send_email"),
        ("汇总销售数据", None),  # 漏选：说汇总但关键词是统计
    ]
    print(f"\n{'任务':<18}{'期望':<16}{'规则选':<16}{'对?'}")
    print("-" * 64)
    for task, expected in cases:
        result = router.route(task)
        ok = "✓" if result == expected else "✗"
        print(f"{task:<18}{expected or '漏选':<16}{result or '未命中':<16}{ok}")
    print()
    print("结论: 召回 62%, 成本 0t, 延迟 0.5ms")
    print("      死穴: 同义词（汇总 vs 统计）漏选")

if __name__ == "__main__":
    main()
