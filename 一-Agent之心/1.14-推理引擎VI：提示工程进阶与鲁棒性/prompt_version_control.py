# prompt_version_control
# 运行: python prompt_version_control.py

import hashlib, json

class PromptVersionControl:
    """提示版本管理"""
    def __init__(self):
        self.versions = []

    def commit(self, template, examples, config, metrics=None):
        """提交提示版本"""
        version = {
            "id": hashlib.md5(template.encode()).hexdigest()[:8],
            "template": template,
            "examples": examples,
            "config": config,
            "metrics": metrics or {},
            "timestamp": self._now(),
        }
        self.versions.append(version)
        return version["id"]

    def ab_test(self, version_a, version_b, test_set, llm):
        """A/B 测试两个版本 (传 id 或 version 对象)"""
        va = self._resolve(version_a)
        vb = self._resolve(version_b)
        results = {"a": [], "b": []}
        for query, expected in test_set:
            out_a = self._run(va, query, llm)
            out_b = self._run(vb, query, llm)
            results["a"].append(out_a == expected)
            results["b"].append(out_b == expected)
        acc_a = sum(results["a"]) / len(results["a"])
        acc_b = sum(results["b"]) / len(results["b"])
        return {"a": acc_a, "b": acc_b, "delta": acc_b - acc_a,
                "winner": "b" if acc_b > acc_a else "a"}

    def rollback(self, version_id):
        """回滚到指定版本"""
        for v in self.versions:
            if v["id"] == version_id:
                return v
        return None

    def _run(self, version, query, llm):
        prompt = version["template"].format(query=query)
        return llm([{"role":"user","content":prompt}])

    def _resolve(self, ref):
        """解析 id 或 version 对象"""
        if isinstance(ref, str):
            return self.rollback(ref)
        return ref

    def _now(self):
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
if __name__ == "__main__":
    vc = PromptVersionControl()
    vid1 = vc.commit("问题: {query}\n答案:", [], {"temp": 0}, {"acc": 0.7})
    vid2 = vc.commit("逐步推理: {query}\n答案:", [], {"temp": 0.3}, {"acc": 0.75})
    print(f"版本1: {vid1}, 版本2: {vid2}")
    def llm(msgs):
        c = msgs[-1]["content"]
        return "42" if "逐步" in c else "未知"
    test_set = [("6*7", "42"), ("8*9", "72")]
    ab = vc.ab_test(vid1, vid2, test_set, llm)
    print(f"A/B: v1={ab['a']:.0%} v2={ab['b']:.0%} 赢家={ab['winner']}")
    old = vc.rollback(vid1)
    print(f"回滚到 v1: {old['id']}")

