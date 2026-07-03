# reflection_search
# 运行: python reflection_search.py

def reflection_search(problem, llm, max_steps=10, max_reflections=3):
    """反思搜索：单链推理 + 错误回退"""
    chain = [{"role": "user", "content": problem}]
    reflection_count = 0

    for step in range(max_steps):
        response = llm(chain)
        if is_satisfactory(response):
            return response

        # 检测是否有错误
        error = detect_error(chain, response)
        if error and reflection_count < max_reflections:
            # 回退到错误发生前
            error_step = locate_error_step(chain, response)
            chain = chain[:error_step]  # 截断错误之后的步骤
            # 添加反思信息
            chain.append({
                "role": "user",
                "content": f"之前的步骤出错: {error}。请修正后继续。"
            })
            reflection_count += 1
        else:
            chain.append({"role": "assistant", "content": response})

    return chain[-1]["content"]
