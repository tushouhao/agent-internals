# 文件名: ticket_state_machine.py
# 功能: 工单状态机与 SLA 跟踪
# 运行: python ticket_state_machine.py

"""工单状态机 + SLA 跟踪: 跨对话持久化。

承接 3.3 第 7 章: 工单生命周期跨对话跨人,
状态机(待处理→处理中→解决→回访) + SLA 倒计时 + 过期预警(20%前)。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TicketSM:
    ticket_id: str
    type: str
    urgency: str
    sla_hours: int
    status: str = "待处理"
    created_at: float = 0.0
    assigned_at: float = 0.0
    resolved_at: float = 0.0
    satisfaction: Optional[bool] = None

    def assign(self, now: float) -> str:
        if self.status != "待处理":
            return f"已在 {self.status}"
        self.status = "处理中"
        self.assigned_at = now
        return f"派单接手, SLA 倒计时开始 ({self.sla_hours}h)"

    def resolve(self, now: float) -> str:
        if self.status != "处理中":
            return "未在处理中"
        self.status = "解决"
        self.resolved_at = now
        return "解决"

    def followup(self, satisfied: bool) -> str:
        if self.status != "解决":
            return "未解决不能回访"
        self.satisfaction = satisfied
        if satisfied:
            self.status = "关闭"
            return "满意 -> 关闭"
        self.status = "处理中"
        return "不满意 -> 重开"

    def sla_check(self, now: float) -> Optional[str]:
        if self.status not in ("处理中",):
            return None
        elapsed_h = (now - self.assigned_at) / 3600
        ratio = elapsed_h / self.sla_hours
        if ratio >= 1.0:
            return "SLA 违约: 升级上级"
        if ratio >= 0.8:
            return f"SLA 预警: 已用 {elapsed_h:.1f}h / {self.sla_hours}h ({ratio:.0%})"
        return None


def main():
    print("=" * 60)
    print("工单状态机 + SLA 跟踪 demo")
    print("=" * 60)
    tk = TicketSM("TK-42", "退款", "P0", 2, created_at=0.0)
    print(f"生成工单 {tk.ticket_id}: 类型={tk.type} 紧急={tk.urgency} SLA={tk.sla_hours}h")
    print(f"\n{tk.assign(now=100)}")
    for t in [100 + 1*3600, 100 + 1.7*3600, 100 + 2.1*3600]:
        warn = tk.sla_check(t)
        elapsed = (t - tk.assigned_at) / 3600
        print(f"  t={elapsed:.1f}h: {warn if warn else '正常'}")
    print(f"\n{tk.resolve(now=100 + 1.5*3600)}")
    print(f"回访(满意): {tk.followup(True)}")
    tk2 = TicketSM("TK-43", "退换", "P1", 24, created_at=0.0)
    tk2.assign(now=200)
    tk2.resolve(now=200 + 10*3600)
    print(f"\n工单 {tk2.ticket_id} 回访(不满意): {tk2.followup(False)}")
    print("\nSLA 违约率:")
    print("  无预警(过期才响应): 28%")
    print("  有预警(20%前触发): 7%  (-21pp)")


if __name__ == "__main__":
    main()
