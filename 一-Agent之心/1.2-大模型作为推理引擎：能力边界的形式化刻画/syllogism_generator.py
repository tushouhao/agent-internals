# 三段论推理题自动生成
# 运行: python syllogism_generator.py

import random, json

# 三段论有效结论推理（简化版规则表）
VALID_CONCLUSIONS = {
    ("All", "All"): "All",
    ("All", "No"):  "No",
    ("No", "All"):  "No",
    ("Some", "All"): "Some",
    ("All", "Some"): "Some",
}

def infer_valid_conclusion(p1, p2):
    """从前提 p1, p2 推断有效结论的量词"""
    q1 = p1.split()[0]
    q2 = p2.split()[0]
    return VALID_CONCLUSIONS.get((q1, q2), "Unknown")

def generate_syllogism():
    """生成三段论推理题"""
    categories = ["All", "No", "Some"]
    subjects = ["A", "B", "C", "X", "Y", "Z"]
    a, b, c = random.sample(subjects, 3)
    p1 = f"{random.choice(categories)} {a} are {b}."
    p2 = f"{random.choice(categories)} {b} are {c}."
    conclusion_q = infer_valid_conclusion(p1, p2)
    conclusion = f"{conclusion_q} {a} are {c}."
    return {"premises": [p1, p2], "conclusion": conclusion}

if __name__ == "__main__":
    random.seed(42)
    for i in range(3):
        s = generate_syllogism()
        print(f"三段论 #{i+1}:")
        print(f"  前提1: {s['premises'][0]}")
        print(f"  前提2: {s['premises'][1]}")
        print(f"  结论:  {s['conclusion']}")
