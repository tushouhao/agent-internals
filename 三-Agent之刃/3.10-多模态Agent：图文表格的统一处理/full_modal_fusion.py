# 文件名: full_modal_fusion.py
# 功能: 三塔门控三模态统一表征，止于三模态齐整召回 + 缺模态退化
# 运行: python full_modal_fusion.py

"""全模态阶：三塔门控把图/文/表拉到同一表征空间，缺模态时降权兜底。"""

import hashlib
import random

random.seed(42)


def mock_embed(text: str, modality: str) -> list:
    """模拟三塔编码器，8 维向量。"""
    h = hashlib.md5((modality + ":" + text).encode()).hexdigest()
    return [(int(h[i:i+2], 16) / 255.0) for i in range(0, 16, 2)]


def quality_score(vec: list) -> float:
    """模态质量分：特征向量能量（L2 范数归一化）。
    生产用模态专属判别器（图像清晰度/文本完备性/表格完整性）。
    """
    return sum(x * x for x in vec) ** 0.5


def gate_weights(img_vec, text_vec, tab_vec, has_img=True, has_text=True, has_tab=True):
    """三塔门控权重：按模态质量 + 是否存在分权重。
    缺模态时该塔权重置 0，剩余塔重新归一化。
    """
    raw = {
        "img": quality_score(img_vec) if has_img else 0.0,
        "text": quality_score(text_vec) if has_text else 0.0,
        "tab": quality_score(tab_vec) if has_tab else 0.0,
    }
    total = sum(raw.values()) + 1e-9
    return {k: v / total for k, v in raw.items()}


def fuse(img_vec, text_vec, tab_vec, has_img=True, has_text=True, has_tab=True):
    """三塔门控融合：联合嵌入 = Σ w_i · v_i。"""
    w = gate_weights(img_vec, text_vec, tab_vec, has_img, has_text, has_tab)
    fused = []
    for a, b, c in zip(img_vec, text_vec, tab_vec):
        val = w["img"] * (a if has_img else 0) + w["text"] * (b if has_text else 0) + w["tab"] * (c if has_tab else 0)
        fused.append(val)
    return fused, w


def simulate_full_modal(n: int = 50) -> dict:
    """全模态阶仿真：三模态齐整召回 + 缺模态退化率。"""
    full_hits = 0
    miss_img_hits = 0
    miss_text_hits = 0
    miss_tab_hits = 0
    for i in range(n):
        q_img = mock_embed(f"查询图_{i}", "image_full")
        q_text = mock_embed(f"查询文_{i}", "text_full")
        q_tab = mock_embed(f"查询表_{i}", "table_full")
        d_img = mock_embed(f"库图_{i}", "image_full")
        d_text = mock_embed(f"库文_{i}", "text_full")
        d_tab = mock_embed(f"库表_{i}", "table_full")
        q_fused, _ = fuse(q_img, q_text, q_tab)
        d_fused, _ = fuse(d_img, d_text, d_tab)
        sim_full = sum(a * b for a, b in zip(q_fused, d_fused))
        if sim_full > 1.8:
            full_hits += 1
        # 缺图
        q_mi, _ = fuse(q_img, q_text, q_tab, has_img=False)
        d_mi, _ = fuse(d_img, d_text, d_tab, has_img=False)
        if sum(a * b for a, b in zip(q_mi, d_mi)) > 1.4:
            miss_img_hits += 1
        # 缺文
        q_mt, _ = fuse(q_img, q_text, q_tab, has_text=False)
        d_mt, _ = fuse(d_img, d_text, d_tab, has_text=False)
        if sum(a * b for a, b in zip(q_mt, d_mt)) > 1.4:
            miss_text_hits += 1
        # 缺表
        q_mr, _ = fuse(q_img, q_text, q_tab, has_tab=False)
        d_mr, _ = fuse(d_img, d_text, d_tab, has_tab=False)
        if sum(a * b for a, b in zip(q_mr, d_mr)) > 1.4:
            miss_tab_hits += 1
    return {
        "full_recall": full_hits / n,
        "miss_img_recall": miss_img_hits / n,
        "miss_text_recall": miss_text_hits / n,
        "miss_tab_recall": miss_tab_hits / n,
        "n": n,
    }


def main():
    """全模态阶 demo：三模态齐整召回 + 缺模态退化率。"""
    r = simulate_full_modal(50)
    print("全模态阶仿真结果（n=50）:")
    print(f"  三模态齐整召回: {r['full_recall']:.0%}（三塔门控对齐）")
    print(f"  缺图召回: {r['miss_img_recall']:.0%}（门控降权退化到文+表）")
    print(f"  缺文召回: {r['miss_text_recall']:.0%}（门控降权退化到图+表）")
    print(f"  缺表召回: {r['miss_tab_recall']:.0%}（门控降权退化到图+文）")
    avg_miss = (r['miss_img_recall'] + r['miss_text_recall'] + r['miss_tab_recall']) / 3
    degrade = avg_miss / r['full_recall']
    print(f"  缺模态召回均值: {avg_miss:.0%}")
    print(f"  缺模态退化率: {degrade:.2f}（缺任一模态召回 / 齐整召回，越近 1 越稳）")
    print(f"  崩溃模式: 权重失衡 + 缺模态退化——门控偏置致一模态独大淹没其余")


if __name__ == "__main__":
    main()
