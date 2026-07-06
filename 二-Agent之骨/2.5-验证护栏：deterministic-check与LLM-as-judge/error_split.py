# 文件名: error_split.py
# 功能: 格式错与语义错两类错误占比与单闸/双闸覆盖率
# 运行: python error_split.py

"""为什么单闸不够：格式错与语义错是两类。

格式错 26%（deterministic 可拦）：JSON 解析失败/Python 语法错/字段缺
语义错 48%（LLM-judge 可拦）：语法对但逻辑错/返回值对但非最优
两类叠加 26%（需双闸）
单闸各只覆盖约一半错误 → 双闸必须叠加。
教学版，模拟错误分布与闸覆盖率。
"""
from dataclasses import dataclass

@dataclass
class ErrorType:
    name: str
    rate: float
    catchable_by: str       # deterministic / llm_judge / both

ERROR_DIST = [
    ErrorType("JSON 解析失败", 0.08, "deterministic"),
    ErrorType("Python 语法错", 0.07, "deterministic"),
    ErrorType("字段缺", 0.06, "deterministic"),
    ErrorType("类型错", 0.05, "deterministic"),
    ErrorType("返回值错", 0.20, "llm_judge"),
    ErrorType("逻辑非最优", 0.15, "llm_judge"),
    ErrorType("边界未处理", 0.13, "llm_judge"),
    ErrorType("格式语义叠加", 0.26, "both"),
]

def coverage(gate: str) -> float:
    """单闸覆盖率：能拦的错误占比。"""
    caught = sum(e.rate for e in ERROR_DIST
                 if gate == e.catchable_by or (gate == "both" and e.catchable_by == "both"))
    return caught

def main():
    print("=" * 64)
    print("格式错与语义错：两类错误与闸覆盖率")
    print("=" * 64)
    print(f"\n{'错误类型':<18}{'占比':<8}{'可拦闸'}")
    print("-" * 64)
    total = 0
    for e in ERROR_DIST:
        print(f"{e.name:<18}{e.rate:<8.0%}{e.catchable_by}")
        total += e.rate
    print(f"{'合计':<18}{total:<8.0%}")
    print()
    det_cov = coverage("deterministic")
    judge_cov = coverage("llm_judge")
    both_cov = coverage("both")
    print("闸覆盖率:")
    print(f"  仅 deterministic: {det_cov:.0%}（拦格式错，拦不住语义错）")
    print(f"  仅 LLM-judge:    {judge_cov:.0%}（拦语义错，拦不住格式错）")
    print(f"  双闸叠加:        {det_cov + judge_cov + both_cov:.0%}（全覆盖）")
    print()
    print("结论: 单闸各只覆盖约一半错误")
    print("      双闸必须叠加, 这是「双闸」的数据基础")

if __name__ == "__main__":
    main()
