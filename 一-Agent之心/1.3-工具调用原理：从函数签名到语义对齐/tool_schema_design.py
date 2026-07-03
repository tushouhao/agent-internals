# 好的 vs 差的工具描述对比
# 运行: python tool_schema_design.py

# 好的 vs 差的工具描述对比
tool_schema_good = {
    "name": "search_products",
    "description": "根据关键词搜索商品，支持分页。返回匹配的商品列表。",
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "搜索关键词，用户输入的原始查询词"
            },
            "page": {
                "type": "integer",
                "description": "页码，从 1 开始",
                "default": 1
            },
        },
        "required": ["keyword"]
    }
}

tool_schema_bad = {
    "name": "search_products",
    "description": "商品搜索接口，支持分页和排序等高级功能，详情参考内部文档。",
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {"type": "string"},
            "page": {"type": "integer"},
        },
        "required": ["keyword"]
    }
}
