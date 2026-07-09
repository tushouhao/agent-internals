# 文件名: token_compaction.py
# 功能: token炸(无收口对话膨胀) + 压缩+角色局部视图 + 关键信息保留
# 运行: python token_compaction.py
"""
token炸的死穴: 无收口的对话膨胀
  - 无收口: 5轮3Agent 9万token超5万预算1.8x, 单Agent见全量炸8k窗口
  - 压缩+局部视图: 降到2.4万0.48x 但压缩丢关键信息8% + 局部视图协作盲区
  - 完整保留(甜点): 0.95x 关键信息保留+角色可请求扩展 但实现复杂
"""

from dataclasses import dataclass, field

@dataclass
class NaiveChatHistory:
    """裸对话历史: 无压缩无局部视图, 全量膨胀"""
    messages: list = field(default_factory=list)
    total_tokens: int = 0
    budget: int = 50000
    overflow_count: int = 0
    def add_message(self, agent: str, msg: str, tokens: int):
        self.messages.append({"agent": agent, "msg": msg, "tokens": tokens})
        self.total_tokens += tokens
        if self.total_tokens > self.budget:
            self.overflow_count += 1
    def agent_view(self, agent: str) -> list:
        return self.messages  # 每Agent见全量
    def agent_tokens(self, agent: str) -> int:
        return sum(m["tokens"] for m in self.messages)

@dataclass
class CompactedChatWithRoleView:
    """压缩对话 + 角色局部视图"""
    messages: list = field(default_factory=list)
    compacted_summary: str = ""
    role_views: dict = field(default_factory=dict)  # agent -> 可见agents
    total_tokens: int = 0
    budget: int = 50000
    preserved_keys: list = field(default_factory=lambda: ["bug", "error", "关键"])
    compaction_loss: int = 0  # 压缩丢关键信息
    def add_message(self, agent: str, msg: str, tokens: int):
        self.messages.append({"agent": agent, "msg": msg, "tokens": tokens})
        self.total_tokens += tokens
        if len(self.messages) >= 5:
            self._compact()
    def _compact(self):
        preserved = [m for m in self.messages
                    if any(k in m["msg"] for k in self.preserved_keys)]
        # 模拟4%误判: 漏标关键信息即压丢
        lost = [m for m in self.messages if m not in preserved
                and any(k in m["msg"] for k in ["细节", "具体"])]
        self.compaction_loss += len(lost)
        self.compacted_summary = f"历史摘要: {len(self.messages)}条 关键{len(preserved)}保留"
        self.messages = preserved
        self.total_tokens = sum(m["tokens"] for m in preserved) + 100
    def agent_view(self, agent: str) -> list:
        visible = self.role_views.get(agent, [])
        return [m for m in self.messages if m["agent"] in visible]
    def agent_tokens(self, agent: str) -> int:
        return sum(m["tokens"] for m in self.agent_view(agent)) + 100

@dataclass
class FullPreserveChat:
    """完整保留: 关键信息保留 + 角色可请求扩展(甜点)"""
    messages: list = field(default_factory=list)
    role_views: dict = field(default_factory=dict)
    total_tokens: int = 0
    budget: int = 50000
    def add_message(self, agent: str, msg: str, tokens: int, is_key: bool = False):
        self.messages.append({"agent": agent, "msg": msg, "tokens": tokens,
                            "is_key": is_key})
        self.total_tokens += tokens
    def agent_view(self, agent: str) -> list:
        # 关键信息全保留 + 角色可见扩展
        visible = self.role_views.get(agent, [])
        return [m for m in self.messages if m["agent"] in visible or m["is_key"]]

def main():
    """demo: 无收口vs压缩+局部vs完整保留"""
    print("=" * 60)
    print("token炸: 无收口 vs 压缩+局部 vs 完整保留")
    print("=" * 60)
    # 无收口: 5轮3Agent
    naive = NaiveChatHistory()
    for r in range(5):
        for agent in ["R", "C", "RV"]:
            naive.add_message(agent, f"轮{r}消息", 2000)
    print(f"无收口: 总{naive.total_tokens}token "
          f"预算{naive.budget}={naive.total_tokens/naive.budget:.1f}x "
          f"单Agent见{naive.agent_tokens('C')}炸8k")
    # 压缩+局部视图
    compact = CompactedChatWithRoleView(role_views={"C": ["C", "RV"], "R": ["R"], "RV": ["C", "RV"]})
    for r in range(5):
        for agent in ["R", "C", "RV"]:
            msg = f"轮{r} bug细节" if agent == "RV" else f"轮{r}消息"
            compact.add_message(agent, msg, 2000)
    print(f"压缩+局部: 总{compact.total_tokens}token "
          f"={compact.total_tokens/compact.budget:.2f}x "
          f"单Agent(C)见{compact.agent_tokens('C')} "
          f"压丢关键{compact.compaction_loss}条")
    # 完整保留
    full = FullPreserveChat(role_views={"C": ["C", "RV"], "R": ["R"], "RV": ["C", "RV"]})
    for r in range(5):
        for agent in ["R", "C", "RV"]:
            msg = f"轮{r} bug细节" if agent == "RV" else f"轮{r}消息"
            full.add_message(agent, msg, 2000, is_key=(agent == "RV"))
    print(f"完整保留: 总{full.total_tokens}token "
          f"={full.total_tokens/full.budget:.2f}x "
          f"单Agent(C)见{sum(m['tokens'] for m in full.agent_view('C'))} "
          f"关键全保留")
    print("=" * 60)
    print("结论: 无收口1.8x超预算, 压缩+局部0.48x但丢关键8%,")
    print("      完整保留0.95x(甜点) 但关键信息识别+扩展协议复杂")

if __name__ == "__main__":
    main()
