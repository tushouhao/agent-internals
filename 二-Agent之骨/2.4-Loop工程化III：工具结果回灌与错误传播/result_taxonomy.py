# 文件名: result_taxonomy.py
# 功能: 工具结果四类异质性分类与处置策略映射
# 运行: python result_taxonomy.py

"""工具结果异质性：四类结果四种处置。

大文本类: 截断+抽取（read_file, web_fetch）
结构化类: 保留+完整性信号（sql_query, list_files）
半结构化类: 抽取 top3（web_search, grep）
布尔+错误类: 只灌清洗后信息（diff_apply, write_file）
教学版，模拟四类结果分布与处置。
"""
from dataclasses import dataclass

@dataclass
class ResultType:
    name: str
    token_range: tuple
    reuse_value: str          # 复用价值
    strategy: str             # 回灌策略
    frequency: float          # 出现频率

FOUR_TYPES = [
    ResultType("大文本", (5000, 50000), "长尾（95% 看 preview）",
               "截断+抽取+引用", 0.55),
    ResultType("结构化", (200, 5000), "高（信息密度高）",
               "保留+完整性信号", 0.20),
    ResultType("半结构化", (300, 2000), "中（噪声多）",
               "抽取 top3", 0.15),
    ResultType("布尔+错误", (50, 300), "低（单次小）",
               "只灌清洗后信息", 0.10),
]

def main():
    print("=" * 72)
    print("工具结果异质性：四类结果四种处置")
    print("=" * 72)
    print(f"\n{'类型':<14}{'token 范围':<18}{'复用价值':<22}{'频率':<8}{'处置策略'}")
    print("-" * 72)
    for t in FOUR_TYPES:
        print(f"{t.name:<14}{str(t.token_range):<18}{t.reuse_value:<22}"
              f"{t.frequency:<8.0%}{t.strategy}")
    print()
    print("关键: naive 一视同仁塞回上下文 = 第一错")
    print("      按类型分处置 = 工程化回灌")
    print("      工具注册时声明 result_type, 按类型选策略而非按工具名硬编码")

if __name__ == "__main__":
    main()
