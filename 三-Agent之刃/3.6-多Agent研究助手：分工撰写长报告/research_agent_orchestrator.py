# 文件名: research_agent_orchestrator.py
# 功能: 多 Agent 研究助手主调度（整合三阶协作+冲突消解的完整混合系统）
# 运行: python research_agent_orchestrator.py
"""多 Agent 研究助手主调度 demo"""

from collections import Counter

SOURCES = [("src1", "智能体定义"), ("src2", "智能体架构"), ("src3", "智能体应用"),
           ("src4", "智能体框架"), ("src5", "智能体评估")]
OUTLINE = ["定义章", "架构章", "应用章", "评估章", "挑战章"]


class ResearchAgent:
    """多 Agent 研究助手主调度: 三阶协作+冲突消解"""

    def __init__(self):
        self.stats = {"single": 0, "pipeline": 0, "parallel": 0, "reject": 0}
        self.resolve_time = 0

    def _judge(self, words: int) -> str:
        if words <= 500:
            return "single"
        if words <= 5000:
            return "pipeline"
        if words <= 20000:
            return "parallel"
        return "reject"

    def _single_draft(self, topic: str, words: int) -> tuple:
        self.stats["single"] += 1
        return (True, f"单Agent直撰{words}字 深度3.4/5 延迟35s", 35, 0)

    def _pipeline_draft(self, topic: str, words: int) -> tuple:
        self.stats["pipeline"] += 1
        src_pkg = {"sources": [t for _, t in SOURCES]}
        outline_pkg = {"outline": OUTLINE[:], "src_ref": src_pkg}
        body_pkg = {"body": "全文", "outline_ref": outline_pkg}
        final_pkg = {"review": "修订", "body_ref": body_pkg}
        for pkg, keys in [(src_pkg, ["sources"]), (outline_pkg, ["outline", "src_ref"]),
                          (body_pkg, ["body", "outline_ref"]), (final_pkg, ["review", "body_ref"])]:
            if not all(k in pkg and pkg[k] for k in keys):
                return (False, "链断包不完整", 0, 0)
        return (True, f"流水线四Agent链式传递完成{words}字 深度4.1/5 延迟45s", 45, 0)

    def _parallel_draft(self, topic: str, words: int) -> tuple:
        self.stats["parallel"] += 1
        writes = [
            {"term": "智能体", "style": "学术"}, {"term": "Agent", "style": "工程"},
            {"term": "智能体", "style": "业务"}, {"term": "Agent", "style": "学术"},
            {"term": "智能体", "style": "工程"},
        ]
        merged = "5章合并"
        terms = [w["term"] for w in writes]
        unified_term = Counter(terms).most_common(1)[0][0]
        unified_style = "学术"
        resolve_t = 6
        self.resolve_time += resolve_t
        return (True, f"并行5Agent分章+合并+消解(术语={unified_term} 风格={unified_style})完成{words}字 深度4.4/5 延迟27s+消解6s", 27, resolve_t)

    def draft(self, topic: str, words: int, depth_req: int = 4) -> tuple:
        stage = self._judge(words)
        if stage == "reject":
            self.stats["reject"] += 1
            return ("reject", "超2万字拒拆分建议拆任务", 0, 0)
        if stage == "single":
            ok, msg, lat, res = self._single_draft(topic, words)
        elif stage == "pipeline":
            ok, msg, lat, res = self._pipeline_draft(topic, words)
        else:
            ok, msg, lat, res = self._parallel_draft(topic, words)
        return ("done" if ok else "fail", msg, lat, res)


def main():
    print("=" * 60)
    print("多 Agent 研究助手主调度 demo")
    print("=" * 60)
    agent = ResearchAgent()
    tests = [
        ("智能体综述", 300, "300字短"),
        ("智能体综述", 3000, "3千字中"),
        ("智能体综述", 8000, "8千字长"),
        ("智能体综述", 15000, "1.5万字长"),
        ("智能体综述", 25000, "2.5万字超长拒"),
    ]
    total_lat, total_res = 0, 0
    for topic, words, label in tests:
        act, msg, lat, res = agent.draft(topic, words)
        total_lat += lat
        total_res += res
        print(f"\n场景: {label} ({words}字)")
        print(f"  -> {act}  延迟={lat}s 消解={res}s")
        print(f"  {msg}")
    print("\n" + "=" * 60)
    print("调度统计:")
    for k, v in agent.stats.items():
        print(f"  {k}: {v}")
    print(f"  总消解耗时: {agent.resolve_time}s")
    print("\n量化基线: 混合综合完成81% 延迟34s 消解12%")
    print("核心KPI: 冲突残留率而非完成率")
    print("         4%残留=精准消解  100%残留=该消不消的割裂")


if __name__ == "__main__":
    main()
