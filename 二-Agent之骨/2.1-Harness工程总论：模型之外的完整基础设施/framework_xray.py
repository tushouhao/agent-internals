# 文件名: framework_xray.py
# 功能: 逆向拆解框架对六大子系统的覆盖度
# 运行: python framework_xray.py

"""框架 X 光：逆向拆解 LangChain/LangGraph/AutoGen 对 harness 的覆盖。

用六大子系统作透镜，看清框架实现了什么、藏起了什么。
教学版，基于公开文档的架构分析。
"""
from dataclasses import dataclass

@dataclass
class FrameworkCoverage:
    name: str
    ctx: str          # 上下文组装
    tool: str         # 工具调度
    error: str        # 错误恢复
    validate: str     # 验证护栏
    state: str        # 状态持久化
    cost: str         # 成本管控
    blind_spot: str   # 盲区

FRAMEWORKS = [
    FrameworkCoverage(
        "LangChain",
        ctx="Memory 类（默认 naive 截断，分层要自写）",
        tool="Tool 抽象（权限检查要自加）",
        error="重试装饰器（熔断逻辑要自写）",
        validate="OutputParser（仅 deterministic check）",
        state="Memory（内存，跨会话要自接 DB）",
        cost="回调统计（熔断要自写）",
        blind_spot="长程任务的上下文压缩、细粒度权限、LLM-as-judge",
    ),
    FrameworkCoverage(
        "LangGraph",
        ctx="State 对象（显式化管理）",
        tool="节点（工具即节点函数）",
        error="边的容错（error edge）",
        validate="路由节点（可插 judge）",
        state="checkpoint（内置持久化）",
        cost="节点统计（细粒度）",
        blind_spot="学习曲线陡，简单任务过度工程",
    ),
    FrameworkCoverage(
        "AutoGen",
        ctx="对话历史（agent 间共享）",
        tool="function_call（WhiteBoard 协调）",
        error="agent 终止条件",
        validate="critic agent（LLM-as-judge 内建）",
        state="对话保存（JSON）",
        cost="token 统计（按 agent）",
        blind_spot="多 agent token 消耗翻倍、调试困难",
    ),
]

def xray(fw: FrameworkCoverage) -> dict:
    """逆向拆解：返回六大子系统覆盖评分。"""
    fields = [fw.ctx, fw.tool, fw.error, fw.validate, fw.state, fw.cost]
    score = 0
    for f in fields:
        if "要自" in f or "要自写" in f or "要自加" in f or "要自接" in f:
            score += 1  # 需自己补
        elif "内置" in f or "内建" in f or "显式" in f:
            score += 3  # 完整实现
        else:
            score += 2  # 基础实现
    return {"覆盖度": score, "需自补数": sum(1 for f in fields if "要自" in f)}

def main():
    print("=" * 78)
    print("框架 X 光：六大子系统覆盖度逆向拆解")
    print("=" * 78)
    for fw in FRAMEWORKS:
        print(f"\n【{fw.name}】")
        print(f"  1.上下文组装: {fw.ctx}")
        print(f"  2.工具调度:   {fw.tool}")
        print(f"  3.错误恢复:   {fw.error}")
        print(f"  4.验证护栏:   {fw.validate}")
        print(f"  5.状态持久化: {fw.state}")
        print(f"  6.成本管控:   {fw.cost}")
        r = xray(fw)
        print(f"  覆盖度评分: {r['覆盖度']}/18, 需自补: {r['需自补数']} 个子系统")
        print(f"  盲区: {fw.blind_spot}")
    print()
    print("拆解法：拿到任何框架，问六个问题——怎么组装上下文/调度工具/")
    print("恢复错误/验证输出/持久化状态/管控成本？六个回答拼出 harness 全貌。")

if __name__ == "__main__":
    main()
