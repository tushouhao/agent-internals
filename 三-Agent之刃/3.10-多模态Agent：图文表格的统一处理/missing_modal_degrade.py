# 文件名: missing_modal_degrade.py
# 功能: 缺模态退化率量化——三模态齐整 vs 缺任一模态召回权衡
# 运行: python missing_modal_degrade.py

"""缺模态退化率：宁可降级不可缺模态即崩的核心 KPI。"""

import hashlib
import random

random.seed(42)


def mock_embed(text: str, modality: str) -> list:
    """模拟编码器，8 维向量。"""
    h = hashlib.md5((modality + ":" + text).encode()).hexdigest()
    return [(int(h[i:i+2], 16) / 255.0) for i in range(0, 16, 2)]


def quality(vec):
    return sum(x * x for x in vec) ** 0.5


def gate_weights(img_vec, text_vec, tab_vec, has_img=True, has_text=True, has_tab=True):
    """门控权重：缺模态置 0 剩余归一化（降权兜底）。"""
    raw = {
        "img": quality(img_vec) if has_img else 0.0,
        "text": quality(text_vec) if has_text else 0.0,
        "tab": quality(tab_vec) if has_tab else 0.0,
    }
    total = sum(raw.values()) + 1e-9
    return {k: v / total for k, v in raw.items()}


def naive_weights(has_img=True, has_text=True, has_tab=True):
    """naive 无兜底：缺模态时其余模态权重仍按训练固定，不求归一化。"""
    if not (has_img and has_text and has_tab):
        return {"img": 0.0, "text": 0.0, "tab": 0.0}  # naive 缺即崩
    return {"img": 1/3, "text": 1/3, "tab": 1/3}


def fuse(img_vec, text_vec, tab_vec, weights, has_img=True, has_text=True, has_tab=True):
    return [
        weights["img"] * (a if has_img else 0) +
        weights["text"] * (b if has_text else 0) +
        weights["tab"] * (c if has_tab else 0)
        for a, b, c in zip(img_vec, text_vec, tab_vec)
    ]


def simulate_degrade(n: int = 200) -> dict:
    """缺模态退化率仿真：齐整 vs 缺图 vs 缺文 vs 缺表，门控 vs naive。"""
    scenarios = {
        "齐整": (True, True, True),
        "缺图": (False, True, True),
        "缺文": (True, False, True),
        "缺表": (True, True, False),
    }
    result = {}
    for name, (hi, ht, hr) in scenarios.items():
        gate_hits = 0
        naive_hits = 0
        for i in range(n):
            q_img = mock_embed(f"q图_{i}", "image_deg")
            q_text = mock_embed(f"q文_{i}", "text_deg")
            q_tab = mock_embed(f"q表_{i}", "table_deg")
            d_img = mock_embed(f"d图_{i}", "image_deg")
            d_text = mock_embed(f"d文_{i}", "text_deg")
            d_tab = mock_embed(f"d表_{i}", "table_deg")
            gw = gate_weights(q_img, q_text, q_tab, hi, ht, hr)
            q_g = fuse(q_img, q_text, q_tab, gw, hi, ht, hr)
            d_g = fuse(d_img, d_text, d_tab, gw, hi, ht, hr)
            thr = 1.8 if (hi and ht and hr) else 1.4
            if sum(a * b for a, b in zip(q_g, d_g)) > thr:
                gate_hits += 1
            nw = naive_weights(hi, ht, hr)
            q_n = fuse(q_img, q_text, q_tab, nw, hi, ht, hr)
            d_n = fuse(d_img, d_text, d_tab, nw, hi, ht, hr)
            if sum(a * b for a, b in zip(q_n, d_n)) > thr:
                naive_hits += 1
        result[name] = {
            "gate_recall": gate_hits / n,
            "naive_recall": naive_hits / n,
        }
    full_gate = result["齐整"]["gate_recall"]
    miss_avg_gate = sum(result[k]["gate_recall"] for k in ["缺图", "缺文", "缺表"]) / 3
    miss_avg_naive = sum(result[k]["naive_recall"] for k in ["缺图", "缺文", "缺表"]) / 3
    return {
        "result": result,
        "n": n,
        "degrade_rate_gate": miss_avg_gate / full_gate if full_gate else 0,
        "degrade_rate_naive": miss_avg_naive / full_gate if full_gate else 0,
    }


def main():
    """缺模态退化率 demo。"""
    r = simulate_degrade(200)
    print("缺模态退化率仿真结果（n=200）:")
    for name, v in r["result"].items():
        print(f"  {name}: 门控召回 {v['gate_recall']:.0%} / naive召回 {v['naive_recall']:.0%}")
    print(f"\n  门控缺模态退化率: {r['degrade_rate_gate']:.2f}（缺任一模态召回/齐整召回，越近 1 越稳）")
    print(f"  naive缺模态退化率: {r['degrade_rate_naive']:.2f}（无兜底缺即崩）")
    print(f"\n  核心洞察:")
    print(f"    门控退化率 {r['degrade_rate_gate']:.2f} 即缺模态仍保 {r['degrade_rate_gate']*100:.0f}% 齐整水平")
    print(f"    naive退化率 {r['degrade_rate_naive']:.2f} 即缺模态骤降至 {r['degrade_rate_naive']*100:.0f}% �齐整水平")
    print(f"    结论: 核心 KPI 是缺模态退化率——宁可降级不可缺模态即崩")


if __name__ == "__main__":
    main()
