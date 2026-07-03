# 符号推理形式化校验器
# 运行: python verify_inference.py

# 符号推理的外部 Verifier 实现
def verify_logical_inference(premises, conclusion, inference_steps):
    """三段论推理的形式化校验"""
    from sympy import symbols, satisfiable
    step_valid = all(is_valid_step(s) for s in inference_steps)
    conclusion_valid = check_entailment(premises, conclusion)
    return step_valid and conclusion_valid
