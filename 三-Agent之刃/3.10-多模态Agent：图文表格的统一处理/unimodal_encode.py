# 文件名: unimodal_encode.py
# 功能: 三模态独立编道（文本/图像/表格），止于模态内召回
# 运行: python unimodal_encode.py

"""单模态阶：每类模态独立编道，不跨模态对齐。"""

import hashlib
import random
from collections import Counter

random.seed(42)


def mock_embed(text: str, modality: str) -> list:
    """模拟模态专属编码器：文本 BERT / 图像 ViT / 表格 TabBERT。
    生产替换为真实模型推理。返回 8 维向量。
    """
    h = hashlib.md5((modality + ":" + text).encode()).hexdigest()
    vec = [(int(h[i:i+2], 16) / 255.0) for i in range(0, 16, 2)]
    return vec


def text_recall(query: str, docs: list) -> float:
    """文本模态内召回：BERT 语义相似度 Top1 命中率。"""
    q = mock_embed(query, "text")
    hits = 0
    for doc in docs:
        d = mock_embed(doc, "text")
        sim = sum(a * b for a, b in zip(q, d)) / (sum(x * x for x in q) * sum(x * x for x in d)) ** 0.5
        if sim > 0.85:
            hits += 1
    return hits / len(docs) if docs else 0.0


def image_recall(query: str, imgs: list) -> float:
    """图像模态内召回：ViT 视觉特征 Top1 命中率。"""
    q = mock_embed(query, "image")
    hits = 0
    for img in imgs:
        d = mock_embed(img, "image")
        sim = sum(a * b for a, b in zip(q, d))
        if sim > 0.8:
            hits += 1
    return hits / len(imgs) if imgs else 0.0


def table_recall(query: str, tables: list) -> float:
    """表格模态内召回：TabBERT 行列关系 Top1 命中率。"""
    q = mock_embed(query, "table")
    hits = 0
    for t in tables:
        d = mock_embed(t, "table")
        sim = sum(a * b for a, b in zip(q, d))
        if sim > 1.2:
            hits += 1
    return hits / len(tables) if tables else 0.0


def simulate_unimodal(n: int = 50) -> dict:
    """单模态阶仿真：三模态各自召回上限。"""
    docs = [f"文档_{i} 内容片段" for i in range(n)]
    imgs = [f"图像_{i} 视觉特征" for i in range(n)]
    tabs = [f"表格_{i} 行列结构" for i in range(n)]
    return {
        "text_recall": text_recall("文档内容", docs),
        "image_recall": image_recall("图像特征", imgs),
        "table_recall": table_recall("表格结构", tabs),
        "n": n,
    }


def main():
    """单模态阶 demo：三模态独立召回。"""
    r = simulate_unimodal(50)
    print("单模态阶仿真结果（n=50）:")
    print(f"  文本召回: {r['text_recall']:.0%}（BERT 模态内，止于一词多义歧义）")
    print(f"  图像召回: {r['image_recall']:.0%}（ViT 模态内，止于一图多物歧义）")
    print(f"  表格召回: {r['table_recall']:.0%}（TabBERT 模态内，止于同表异义歧义）")
    print(f"  崩溃模式: 模态内歧义——纯文不能跨图、纯图不能跨表、纯表不能跨文")
    avg = (r['text_recall'] + r['image_recall'] + r['table_recall']) / 3
    print(f"  模态内召回均值: {avg:.0%}（止于此，跨模态要 2 章拆对齐）")


if __name__ == "__main__":
    main()
