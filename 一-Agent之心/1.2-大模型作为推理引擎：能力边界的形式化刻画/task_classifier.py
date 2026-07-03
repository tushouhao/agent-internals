# 推理任务四象限分类器
# 运行: python task_classifier.py

from enum import Enum

class TaskQuadrant(Enum):
    LOW_LOW = "Q1"     # 低复杂度 + 封闭知识
    HIGH_LOW = "Q2"    # 高复杂度 + 封闭知识
    LOW_OPEN = "Q3"    # 低复杂度 + 开放知识
    HIGH_OPEN = "Q4"   # 高复杂度 + 开放知识

def classify_task(task_desc, complexity_fn, knowledge_fn):
    """将推理任务分类到四象限"""
    c = complexity_fn(task_desc)   # 返回 'low' 或 'high'
    k = knowledge_fn(task_desc)    # 返回 'closed' 或 'open'
    mapping = {('low','closed'): TaskQuadrant.LOW_LOW,
               ('high','closed'): TaskQuadrant.HIGH_LOW,
               ('low','open'): TaskQuadrant.LOW_OPEN,
               ('high','open'): TaskQuadrant.HIGH_OPEN}
    return mapping.get((c, k))

if __name__ == "__main__":
    def cx(t):
        # 简单启发式: 超过 10 字认为是高复杂度
        return "high" if len(t) > 10 else "low"
    def kn(t):
        # 含"设计"/"创造"认为是开放知识
        return "open" if any(w in t for w in ["设计", "创造", "提出"]) else "closed"

    tasks = [
        "查订单",
        "设计一个 RAG 系统",
        "计算 2+2",
        "提出新的推荐算法",
    ]
    print("推理任务四象限分类:")
    for t in tasks:
        q = classify_task(t, cx, kn)
        print(f"  '{t}' -> {q.name} ({q.value})")
