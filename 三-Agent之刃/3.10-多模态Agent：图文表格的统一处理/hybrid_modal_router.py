# 文件名: hybrid_modal_router.py
# 功能: 按输入模态构成判别分流三级 + 模态缺失超限拒答
# 运行: python hybrid_modal_router.py

"""混合路由器：模态构成判别 + 质量门控 + 分流三级 + 拒答护栏。"""

import hashlib
import random

random.seed(42)


def mock_embed(text: str, modality: str) -> list:
    """模拟编码器，8 维向量。"""
    h = hashlib.md5((modality + ":" + text).encode()).hexdigest()
    return [(int(h[i:i+2], 16) / 255.0) for i in range(0, 16, 2)]


def detect_modalities(img=None, text=None, table=None):
    """检测输入模态构成。"""
    mods = []
    if img is not None:
        mods.append("image")
    if text is not None:
        mods.append("text")
    if table is not None:
        mods.append("table")
    return mods


def quality_gate(vec, modality):
    """模态质量分门控。"""
    score = sum(x * x for x in vec) ** 0.5
    return score, score >= 0.3


def route(img=None, text=None, table=None):
    """路由判别：返回走哪级 + 是否拒答。
    返回 (stage, reject, reason)
    """
    mods = detect_modalities(img, text, table)
    if len(mods) == 0:
        return "none", True, "无模态输入"
    reject = False
    for m in mods:
        src = {"image": img, "text": text, "table": table}[m]
        v = mock_embed(src, m + "_q")
        _, ok = quality_gate(v, m)
        if not ok:
            reject = True
    if reject:
        return "none", True, "模态质量低于 0.3 阈值"
    if len(mods) == 1:
        return "unimodal", False, f"单模态 {mods[0]}"
    if len(mods) == 2:
        return "cross", False, f"双模态 {mods}"
    return "full", False, f"三模态齐整"


def simulate_router(n: int = 90) -> dict:
    """混合路由器仿真：90 任务分流统计。"""
    stages = {"unimodal": 0, "cross": 0, "full": 0, "none": 0}
    recalls = {"unimodal": [], "cross": [], "full": []}
    latencies = {"unimodal": [], "cross": [], "full": []}
    recall_base = {"unimodal": 0.88, "cross": 0.83, "full": 0.79}
    latency_base = {"unimodal": 200, "cross": 900, "full": 2200}
    for i in range(n):
        r = random.random()
        if r < 0.33:
            stage, rej, _ = route(text=f"纯文_{i}")
        elif r < 0.66:
            stage, rej, _ = route(img=f"图_{i}", text=f"文_{i}")
        else:
            stage, rej, _ = route(img=f"图_{i}", text=f"文_{i}", table=f"表_{i}")
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        recalls[stage].append(recall_base[stage] + random.uniform(-0.03, 0.03))
        latencies[stage].append(latency_base[stage] + random.randint(-50, 50))
    total_runs = sum(len(v) for v in recalls.values())
    avg_recall = sum(sum(v) for v in recalls.values()) / max(1, total_runs)
    avg_latency = sum(sum(v) for v in latencies.values()) / max(1, total_runs)
    return {
        "stages": stages,
        "n": n,
        "avg_recall": avg_recall,
        "avg_latency": avg_latency,
        "reject_rate": stages["none"] / n,
    }


def main():
    """混合路由器 demo：90 任务分流。"""
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流统计: 单模态 {r['stages']['unimodal']} / 跨模态 {r['stages']['cross']} / 全模态 {r['stages']['full']} / 拒答 {r['stages']['none']}")
    print(f"  综合对齐召回: {r['avg_recall']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}ms")
    print(f"  拒答率: {r['reject_rate']:.0%}（模态缺失或质量低于 0.3 拒答）")
    print(f"  对比全全模态: 召回 79% 延迟 2200ms → 混合召回 {r['avg_recall']:.0%} 延迟 {r['avg_latency']:.0f}ms")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/2200)*100:.0f}% 召回不牺牲")


if __name__ == "__main__":
    main()
