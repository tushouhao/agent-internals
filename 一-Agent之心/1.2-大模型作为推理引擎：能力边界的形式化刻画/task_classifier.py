# 推理任务四象限分类器
# 运行: python task_classifier.py

# 推理任务分类器
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
