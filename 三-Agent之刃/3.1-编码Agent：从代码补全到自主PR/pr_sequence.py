# 文件名: pr_sequence.py
# 功能: PR 级多提交序列与评审反馈循环
# 运行: python pr_sequence.py

"""PR 级: 多提交边界规划 + 评审反馈循环。

承接 3.1 第 4 章: 多提交序列的语义连贯是 PR 级核心能力,
有提交边界规划的 PR 评审通过率 61% vs 无规划 34%。
反馈分类(accept/request_changes/comment-only)误判率 7%。
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Commit:
    """单提交: 语义 + diff + 涉及文件。"""
    message: str
    files: List[str]
    diff: str
    reviewed: bool = False
    accepted: bool = False


@dataclass
class ReviewFeedback:
    """评审反馈: 按提交粒度给意见。"""
    commit_idx: int
    comment: str
    action: str  # accept / request_changes / comment


@dataclass
class PRAgent:
    """PR 级编码 Agent: 规划提交序列 + 评审循环。"""
    commits: List[Commit] = field(default_factory=list)
    reviews: List[ReviewFeedback] = field(default_factory=list)
    revision_round: int = 0
    max_revisions: int = 3

    def plan_commits(self, issue: str) -> List[Commit]:
        """规划提交序列: 拆成语义独立提交。"""
        plan = [
            Commit("feat(auth): add captcha param to login", ["auth.py"], "def login(u,p,captcha):"),
            Commit("refactor(routes): pass captcha in login call", ["routes.py"], "login(u,p,req.captcha)"),
            Commit("test(auth): cover captcha path", ["tests/test_auth.py"], "+def test_login_captcha"),
            Commit("docs(api): document captcha param", ["docs/api.md"], "+captcha: str"),
        ]
        self.commits = plan
        return plan

    def push(self) -> str:
        return f"git push {len(self.commits)} commits"

    def handle_review(self, feedbacks: List[ReviewFeedback]) -> bool:
        """处理评审: 接受的标记, 要求改的修订。"""
        self.revision_round += 1
        for fb in feedbacks:
            if fb.action == "accept":
                self.commits[fb.commit_idx].reviewed = True
                self.commits[fb.commit_idx].accepted = True
            elif fb.action == "request_changes":
                rev = Commit(f"fix: address review on commit {fb.commit_idx+1}",
                             self.commits[fb.commit_idx].files, f"修订: {fb.comment}")
                self.commits.append(rev)
        all_accepted = all(c.accepted for c in self.commits if c.reviewed)
        return all_accepted and self.revision_round <= self.max_revisions


def main():
    print("=" * 60)
    print("PR 级多提交序列与评审循环 demo")
    print("=" * 60)
    agent = PRAgent()
    plan = agent.plan_commits("Issue #42: login 加 captcha")
    print("提交序列规划:")
    for i, c in enumerate(plan):
        print(f"  提交{i+1}: {c.message} ({c.files})")
    print(f"\n{agent.push()}")
    fbs = [
        ReviewFeedback(0, "签名 OK", "accept"),
        ReviewFeedback(1, "调用方要加空 captcha fallback", "request_changes"),
        ReviewFeedback(2, "测试 OK", "accept"),
        ReviewFeedback(3, "文档 OK", "accept"),
    ]
    print("\n第一轮评审反馈:")
    for fb in fbs:
        print(f"  提交{fb.commit_idx+1}: {fb.action} - {fb.comment}")
    agent.handle_review(fbs)
    print(f"\n修订后提交数: {len(agent.commits)} (新增修订提交)")
    print(f"修订轮: {agent.revision_round} / {agent.max_revisions}")
    print("\nPR 评审通过率:")
    print(f"  无提交边界规划 (一锅烩): 34%")
    print(f"  有提交边界规划 (拆提交): 61%  (+27pp)")


if __name__ == "__main__":
    main()
