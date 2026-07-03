# write_filter
# 运行: python write_filter.py

import re, time

class WriteFilter:
    """写入内容三层过滤器"""
    def __init__(self, llm_extract=None):
        self.llm_extract = llm_extract
        self.noise_patterns = [r'^(好的|嗯|是的|收到|谢谢|不好意思)[！。!?]?$',
                               r'^(哈哈|呵呵|嘿)[！!]?$', r'^\s*$']
        self.duplicate_cache = set()

    def filter(self, message, context=None):
        content = message.get("content", "").strip()
        if self._is_noise(content):
            return {"action": "drop", "reason": "noise"}
        if self._is_duplicate(content):
            return {"action": "drop", "reason": "duplicate"}
        purified = self._purify(content)
        metadata = self._annotate(message, purified, context)
        return {"action": "write", "content": purified, "metadata": metadata}

    def _is_noise(self, content):
        return any(re.match(p, content) for p in self.noise_patterns)

    def _is_duplicate(self, content):
        sig = hash(content[:50])
        if sig in self.duplicate_cache:
            return True
        self.duplicate_cache.add(sig)
        return False

    def _purify(self, content):
        cleaned = re.sub(r'(那个|这个|就是说|然后呢|你知道的)', '', content)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if self.llm_extract and len(cleaned) > 100:
            return self.llm_extract(cleaned)
        return cleaned

    def _annotate(self, message, content, context):
        mtype = self._classify_type(content)
        return {"type": mtype, "importance": self._score_importance(content, mtype),
                "role": message.get("role"), "timestamp": time.time(),
                "has_number": bool(re.search(r'\d{3,}', content)),
                "has_id": bool(re.search(r'[A-Z]{2,}\d+', content))}

    def _classify_type(self, content):
        if re.search(r'\d{3,}|[A-Z]{2,}\d+', content): return "fact"
        if any(kw in content for kw in ["喜欢", "偏好", "希望", "要求"]): return "preference"
        if any(kw in content for kw in ["错误", "失败", "问题", "异常"]): return "error"
        if any(kw in content for kw in ["决策", "选择", "决定"]): return "decision"
        return "general"

    def _score_importance(self, content, mtype):
        base = {"fact": 0.8, "preference": 0.7, "error": 0.9,
                "decision": 0.85, "general": 0.3}.get(mtype, 0.3)
        if re.search(r'\d{3,}|[A-Z]{2,}\d+', content):
            base = min(1.0, base + 0.1)
        return base

if __name__ == "__main__":
    wf = WriteFilter()
    msgs = [{"content":"好的"},{"content":"订单 OD2024001 金额 12500"},
            {"content":"订单 OD2024001 金额 12500"},
            {"content":"那个 就是说 我希望加急发货"},
            {"content":""}]
    for m in msgs:
        r = wf.filter(m)
        print(f"  '{m['content'][:20]}': {r['action']} {r.get('reason','')}")
        if r['action']=='write':
            print(f"    -> {r['content'][:40]} | {r['metadata']}")

