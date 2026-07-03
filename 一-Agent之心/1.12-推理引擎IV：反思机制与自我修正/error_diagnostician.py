# error_diagnostician
# 运行: python error_diagnostician.py

class ErrorDiagnostician:
    """错误诊断器: 四种信号"""
    def diagnose(self, action, task, signal_type="external"):
        if signal_type == "external":
            return self._external_test(action, task)
        elif signal_type == "internal":
            return self._internal_review(action, task)
        elif signal_type == "trace":
            return self._trace_replay(action, task)
        elif signal_type == "contrast":
            return self._contrast_example(action, task)
        return {"score": 0.5, "feedback": "无信号"}

    def _external_test(self, action, task):
        """外部信号: 测试用例"""
        tests = task.get("tests", [])
        passed, failed = 0, []
        for t in tests:
            try:
                result = eval(action, {"__builtins__": {}}, {})
                if result == t["expected"]: passed += 1
                else: failed.append(t["name"])
            except Exception as e:
                failed.append(f"{t['name']}: {type(e).__name__}")
        score = passed / max(len(tests), 1)
        return {"score": score, "feedback": f"通过{passed}/{len(tests)}, 失败: {failed}"}

    def _internal_review(self, action, task):
        """内部审查: LLM 自评"""
        prompt = f"任务: {task.get('desc','')}\n方案: {action[:300]}\n列出 3 个潜在问题。"
        issues = self.llm([{"role":"user","content":prompt}]).split('\n')
        score = max(0, 1 - len(issues) * 0.2)
        return {"score": score, "feedback": "; ".join(issues[:3])}

    def _trace_replay(self, action, task):
        """轨迹回放: 检查中间步骤"""
        steps = action.split('|')
        problematic = [i for i, s in enumerate(steps) if 'error' in s.lower() or 'fail' in s.lower()]
        score = 1 - len(problematic) / max(len(steps), 1)
        return {"score": score, "feedback": f"问题步骤: {problematic}"}

    def _contrast_example(self, action, task):
        """对比样例: 与正确示例对比"""
        example = task.get("example", "")
        overlap = len(set(action.split()) & set(example.split())) / max(len(set(example.split())), 1)
        return {"score": overlap, "feedback": f"与样例重合度: {overlap:.0%}"}

    def llm(self, msgs): return "问题1\n问题2\n问题3"
if __name__ == "__main__":
    d = ErrorDiagnostician()
    task = {"desc": "求和", "tests": [{"name":"t1","expected":10}], "example": "1+2+3+4=10"}
    for sig in ["external", "internal", "trace", "contrast"]:
        r = d.diagnose("10", task, sig)
        print(f"{sig}: score={r['score']:.2f} feedback={r['feedback'][:40]}")

