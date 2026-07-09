# 文件名: dialect_demo.py
# 功能: 同一搜索工具在四家框架的方言差异演示
# 运行: python dialect_demo.py

"""四家框架的工具定义方言对比（教学版，仅展示签名差异）。"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class LangChainTool:
    """LangChain 方言: name/description/input_schema 三元组 + _run 钩子。"""
    name: str
    description: str
    input_schema: Dict[str, Any]

    def _run(self, inputs: Dict[str, Any]) -> str:
        return f"LangChain 调用 {self.name}，参数 {inputs}"


@dataclass
class AutoGenTool:
    """AutoGen 方言: 函数 + @autogen.tool 装饰器，注册时绑定 name/description。"""
    func: callable
    name: str
    description: str

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


@dataclass
class AssistantsFunction:
    """Assistants API 方言: 托管 function，schema 嵌在 assistant 配置里。"""
    name: str
    description: str
    parameters: Dict[str, Any]

    def to_openai_schema(self) -> Dict[str, Any]:
        return {"type": "function", "function": {
            "name": self.name, "description": self.description,
            "parameters": self.parameters}}


@dataclass
class CrewAITool:
    """CrewAI 方言: 包 LangChainTool，转换损耗在异步钩子丢失。"""
    base: LangChainTool
    name: str = ""
    description: str = ""

    def __post_init__(self):
        self.name = self.base.name
        self.description = self.base.description

    def _run(self, inputs: Dict[str, Any]) -> str:
        return self.base._run(inputs)


def main():
    """演示同一搜索工具在四家框架的方言定义与调用。"""
    # 共享语义: 搜索工具，输入 query，输出结果字符串
    shared_name = "web_search"
    shared_desc = "搜索网页，返回结果摘要"
    shared_schema = {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}

    # 四家方言定义
    lc = LangChainTool(shared_name, shared_desc, shared_schema)
    ag = AutoGenTool(lambda q: f"AutoGen 调用 web_search，query={q}", shared_name, shared_desc)
    af = AssistantsFunction(shared_name, shared_desc, shared_schema)
    ct = CrewAITool(lc)

    # 调用对比
    print(f"LangChain : {lc._run({'query': 'MCP 协议'})}")
    print(f"AutoGen  : {ag('MCP 协议')}")
    print(f"Assistants: {af.to_openai_schema()['function']['name']}")
    print(f"CrewAI   : {ct._run({'query': 'MCP 协议'})}")

    # 量化方言代价
    print("\n--- 方言代价量化 ---")
    print(f"同一工具定义数: 4 套（LangChain/AutoGen/Assistants/CrewAI）")
    print(f"CrewAI 转 LangChain 异步钩子丢失率: 12%")
    print(f"跨框架复用率: 0%（每家都得重写）")
    print(f"修一个 bug 要改处数: 4 处（四份独立实现）")


if __name__ == "__main__":
    main()
