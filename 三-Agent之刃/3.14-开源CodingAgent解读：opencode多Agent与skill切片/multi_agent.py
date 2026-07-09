# 文件名: multi_agent.py
# 功能: 主子委托协议 + 回执仲裁四态，止于回执失真率
# 运行: python multi_agent.py

"""多 Agent 阶：主子委托 + 回执仲裁，崩在回执失真。"""

import random
import json
import hashlib

random.seed(42)


def delegate_task(task: str, ctx: str, budget: int) -> dict:
    """主→子委托协议三件套（task+ctx+budget 序列化契约）。"""
    payload = {"task": task, "ctx": ctx, "budget": budget}
    return {"task": task, "ctx": ctx, "budget": budget, "hash": hashlib.md5(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()}


def sub_agent_execute(delegation: dict) -> dict:
    """子 Agent 执行回执四态（完成/部分/失败/越界）。"""
    r = random.random()
    if r < 0.65:
        return {"status": "ok", "result": "完成"}
    elif r < 0.80:
        return {"status": "partial", "result": "部分"}
    elif r < 0.92:
        return {"status": "fail", "result": "失败"}
    else:
        return {"status": "out_of_bounds", "result": "越界"}


def arbitrate_return(ret: dict, inject_distortion: bool = False) -> dict:
    """回执仲裁四态判别。模拟 22% 失真（部分误判为完成/越界误判为失败）。"""
    if inject_distortion:
        if ret["status"] == "partial":
            ret = dict(ret)
            ret["status"] = "ok"
        elif ret["status"] == "out_of_bounds":
            ret = dict(ret)
            ret["status"] = "fail"
    return {"arbitrated": ret["status"], "is_distortion": inject_distortion}


def simulate_multi(n: int = 50) -> dict:
    """多 Agent 阶仿真：50 任务续跑率 + 回执失真率。"""
    ok = 0
    distortion = 0
    for i in range(n):
        delegation = delegate_task(f"子任务_{i}", "ctx切片", 1000)
        ret = sub_agent_execute(delegation)
        inject = random.random() < 0.22
        arb = arbitrate_return(ret, inject_distortion=inject)
        if arb["arbitrated"] == "ok" and not arb["is_distortion"]:
            ok += 1
        if arb["is_distortion"]:
            distortion += 1
    return {"resume_rate": ok / n, "distortion_rate": distortion / n, "n": n}


def main():
    """多 Agent 阶 demo。"""
    r = simulate_multi(50)
    print("多 Agent 阶仿真结果（n=50）:")
    print(f"  续跑率: {r['resume_rate']:.0%}（主子委托+回执仲裁）")
    print(f"  回执失真率: {r['distortion_rate']:.0%}（部分误判为完成/越界误判为失败）")
    print(f"  崩溃模式: 回执失真——误判致续跑错步骤交付漏")


if __name__ == "__main__":
    main()
