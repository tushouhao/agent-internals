# 文件名: ctx_isolation.py
# 功能: 子 Agent ctx 三层边界 + 三类泄漏防线骨架
# 运行: python ctx_isolation.py

"""上下文隔离: 三层边界（task ctx/loop state/tool registry）+ 三类泄漏防线。"""

from dataclasses import dataclass, field
import copy
from typing import Any, Dict, List, Tuple


@dataclass
class ParentCtx:
    """主 Agent 上下文（简化教学版）。"""
    history: List[str]
    loop_state: str
    tools: Dict[str, Any]
    private_tools: List[str]


@dataclass
class SubAgentCtx:
    """子 Agent 上下文（三层隔离后的副本）。"""
    history: List[str]
    loop_state: str = "idle"
    tools: Dict[str, Any] = field(default_factory=dict)
    is_destroyed: bool = False


def isolate_task_ctx(parent: ParentCtx, relevant_slice: List[str]) -> List[str]:
    """task ctx 隔离: 深拷贝相关切片（防引用泄漏）。"""
    return copy.deepcopy([h for h in parent.history if h in relevant_slice])


def isolate_loop_state() -> str:
    """loop state 隔离: 子 Agent 独立 7 状态机，初态 idle。"""
    return "idle"


def isolate_tool_registry(parent: ParentCtx, allowed_tools: List[str]) -> Dict[str, Any]:
    """tool registry 隔离: 子 Agent 独立工具白名单（防越权访问）。"""
    isolated = {}
    for name in allowed_tools:
        if name in parent.private_tools:
            continue
        if name in parent.tools:
            isolated[name] = copy.deepcopy(parent.tools[name])
    return isolated


def destroy_sub_ctx(sub: SubAgentCtx) -> None:
    """子 Agent 销毁: 防残留泄漏（gc + ctx 清零）。"""
    sub.history.clear()
    sub.tools.clear()
    sub.loop_state = "destroyed"
    sub.is_destroyed = True


def main():
    """三层边界与三类泄漏防线演示。"""
    parent = ParentCtx(
        history=["用户问: 比价", "主 Agent 已拆 5 URL", "主 Agent 派子 A 抓 u1"],
        loop_state="tool_calling",
        tools={"fetch_url": object, "parse_price": object, "private_admin": object},
        private_tools=["private_admin"])

    print("=== 三层边界隔离演示 ===")

    sub_history = isolate_task_ctx(parent, ["用户问: 比价", "主 Agent 已拆 5 URL"])
    print(f"件一 task ctx 隔离: 子 ctx = {sub_history}")
    print(f"  防引用泄漏: 深拷贝副本，子改不影响主（主 history 不变: {parent.history}）")
    sub_history.append("子 Agent 自己的记录")
    print(f"  验证: 子改后主 history 仍不变: {parent.history}")

    sub_state = isolate_loop_state()
    print(f"\n件二 loop state 隔离: 子 state = {sub_state}（主 state = {parent.loop_state}）")
    print(f"  �残留泄漏: 子独立 7 状态机，销毁后清零不残留主 ctx")

    sub_tools = isolate_tool_registry(parent, ["fetch_url", "parse_price", "private_admin"])
    print(f"\n件三 tool registry 隔离: 子 tools = {list(sub_tools.keys())}")
    print(f"  防越权访问: private_admin 在白名单但被拒（主 private_tools 过滤）")

    print("\n=== 三类泄漏防线 ===")
    print(f"{'泄漏':8s} | {'防线':24s} | {'动作':20s} | 承接")
    print(f"{'引用泄漏':8s} | {'task ctx 隔离':24s} | {'深拷贝 + 序列化':20s} | 2.4 工具回灌")
    print(f"{'残留泄漏':8s} | {'loop state 隔离':24s} | {'销毁 + gc + 清零':20s} | 2.2 7 状态机")
    print(f"{'越权访问':8s} | {'tool registry 隔离':24s} | {'白名单 + 越权拒绝':20s} | 2.6 Skill 注册")

    sub = SubAgentCtx(history=sub_history, loop_state="tool_calling", tools=sub_tools)
    print(f"\n=== 子 Agent 销毁（防残留泄漏）===")
    print(f"销毁前: history={sub.history}, tools={list(sub.tools.keys())}, state={sub.loop_state}")
    destroy_sub_ctx(sub)
    print(f"销毁后: history={sub.history}, tools={list(sub.tools.keys())}, state={sub.loop_state}, destroyed={sub.is_destroyed}")


if __name__ == "__main__":
    main()
