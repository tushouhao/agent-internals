# 三段论推理题自动生成
# 运行: python syllogism_generator.py

import random, json

def generate_syllogism():
    """生成三段论推理题"""
    categories = ["All", "No", "Some"]
    subjects = ["A", "B", "C", "X", "Y", "Z"]
    a, b, c = random.sample(subjects, 3)
    p1 = f"{random.choice(categories)} {a} are {b}."
    p2 = f"{random.choice(categories)} {b} are {c}."
    conclusion = infer_valid_conclusion(p1, p2)
    return {"premises": [p1, p2], "conclusion": conclusion}
