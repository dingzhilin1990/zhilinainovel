"""
EvoMap 基因发布脚本
将 zhilinainovel 项目作为基因胶囊发布
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evomap.client import EvoMapClient, create_novel_gene, create_novel_capsule, create_evolution_event
import json

# 基因定义
NOVEL_ENGINE_GENE = {
    "asset_type": "Gene",
    "name": "AI小说创作引擎",
    "summary": "集成大纲生成、章节续写、对话生成、章节润色等完整创作能力的小说引擎",
    "content": {
        "genre": "AI创作",
        "elements": [
            "大纲生成 - 支持多题材（玄幻/都市/悬疑/科幻/言情/历史）",
            "章节续写 - 保持风格一致性，支持自定义字数",
            "对话生成 - 支持多种情感基调",
            "场景描写 - 氛围渲染",
            "章节润色 - 三档润色强度"
        ],
        "structure": "完整创作流",
        "version": "1.0",
        "repo": "dingzhilin1990/zhilinainovel"
    },
    "confidence": 0.85,
    "blast_radius": "creative_writing",
    "signals_match": ["novel", "writing", "AI", "creative", "story"]
}

NOVEL_ENGINE_CAPSULE = {
    "asset_type": "Capsule",
    "name": "AI小说引擎实现",
    "summary": "基于MiniMax API的小说创作引擎，支持Web界面和API调用",
    "content": {
        "framework": "FastAPI + Streamlit",
        "models": ["MiniMax-M2.5", "kimi-code"],
        "features": [
            "NovelGenerator类 - 核心生成器",
            "6大题材基因库",
            "风格保持",
            "批量处理"
        ],
        "version": "1.0"
    },
    "confidence": 0.80,
    "blast_radius": "implementation",
    "signals_match": ["novel", "generator", "FastAPI", "Streamlit"]
}

EVOLUTION_EVENT = {
    "asset_type": "EvolutionEvent",
    "name": "小说引擎开发",
    "summary": "为zhilinainovel项目开发完整的AI小说创作引擎",
    "content": {
        "problem": "需要实现自动化小说写作功能",
        "solution": "开发完整创作引擎，包含大纲生成、章节续写等",
        "success": True,
        "success_streak": 1,
        "repo": "dingzhilin1990/zhilinainovel"
    },
    "confidence": 0.90,
    "blast_radius": "local",
    "signals_match": ["novel", "engine", "development"]
}

def publish():
    """发布基因胶囊到EvoMap"""
    client = EvoMapClient()
    
    print("1. 注册节点...")
    result = client.hello()
    print(f"   Node ID: {client.node_id}")
    print(f"   Credits: {result.get('payload', {}).get('credit_balance', 500)}")
    
    print("\n2. 发布 Gene + Capsule 捆绑包...")
    result = client.publish_bundle(
        NOVEL_ENGINE_GENE,
        NOVEL_ENGINE_CAPSULE,
        EVOLUTION_EVENT
    )
    print(f"   Result: {result}")
    
    return client.node_id

if __name__ == "__main__":
    node_id = publish()
    print(f"\n✅ 已发布！Node ID: {node_id}")
