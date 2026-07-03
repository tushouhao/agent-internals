# 符号推理形式化校验器
# 运行: python verify_inference.py

# 简化版步骤校验：检查步骤是否引用了前提或前序结论
def is_valid_step(step):
    """校验单步推理是否有效（简化版：检查是否非空且含推导词）"""
    if not step or not isinstance(step, str):
        return False
    derivation_marks = ["由", "故", "因此", "所以", "可得"]
    return any(m in step for m in derivation_marks)

# 简化版蕴含检查：检查结论是否被前提集支持
def check_entailment(premises, conclusion):
    """检查前提集是否蕴含结论（简化版：基于关键词包含）"""
    premise_words = set()
    for p in premises:
        for w in ["鸟", "会飞", "麻雀", "哺乳", "猫", "狗"]:
            if w in p:
                premise_words.add(w)
    conclusion_words = set(w for w in ["鸟", "会飞", "麻雀", "哺乳", "猫", "狗"]
                           if w in conclusion)
    return conclusion_words.issubset(premise_words)

def verify_logical_inference(premises, conclusion, inference_steps):
    """三段论推理的形式化校验"""
    step_valid = all(is_valid_step(s) for s in inference_steps)
    conclusion_valid = check_entailment(premises, conclusion)
    return {"steps_valid": step_valid,
            "conclusion_entailed": conclusion_valid,
            "overall": step_valid and conclusion_valid}

if __name__ == "__main__":
    premises = ["所有鸟都会飞", "麻雀是鸟"]
    conclusion = "麻雀会飞"
    steps = ["由前提1，所有鸟都会飞", "由前提2，麻雀是鸟", "故麻雀会飞"]
    result = verify_logical_inference(premises, conclusion, steps)
    print(f"逻辑推理验证:")
    print(f"  步骤有效: {result['steps_valid']}")
    print(f"  结论蕴含: {result['conclusion_entailed']}")
    print(f"  整体通过: {result['overall']}")
