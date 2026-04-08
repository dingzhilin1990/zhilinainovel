"""
zhilinainovel - FastAPI Server
AI小说创作助手 - REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

# Lazy import to avoid crashing on startup without API key
_client = None

def get_client():
    """Lazy initialization of OpenAI-compatible client."""
    global _client
    if _client is None:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("MINIMAX_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.minimax.chat/v1")

        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="API key not configured. Set OPENAI_API_KEY or MINIMAX_API_KEY env var."
            )

        _client = OpenAI(api_key=api_key, base_url=base_url)

    return _client

def get_model() -> str:
    return os.getenv("MODEL", "MiniMax-M2.5")

# ============ App Setup ============

app = FastAPI(
    title="zhilinainovel",
    description="AI小说创作助手 API",
    version="0.2.0"
)

# CORS for Streamlit and other frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Data Models ============

class AnalyzeRequest(BaseModel):
    content: str
    genre: Optional[str] = None

class GenerateStoryRequest(BaseModel):
    genre: str
    theme: str
    main_char: str
    length: str = "短篇"  # 短篇/中篇/长篇/超长篇

class GenerateChapterRequest(BaseModel):
    outline: str
    previous_content: str = ""
    genre: str = "都市"
    style_genes: Optional[dict] = None
    word_count: int = 2000

class DialogueRequest(BaseModel):
    character1: str
    character2: str
    context: str
    emotion: str = "normal"

class PolishRequest(BaseModel):
    content: str
    level: str = "medium"  # light/medium/heavy

# ============ Health & Info ============

@app.get("/")
def root():
    return {
        "message": "zhilinainovel API",
        "version": "0.2.0",
        "configured": bool(os.getenv("OPENAI_API_KEY") or os.getenv("MINIMAX_API_KEY")),
        "model": get_model()
    }

@app.get("/health")
def health():
    try:
        get_client()
        return {"status": "ok", "api": "connected"}
    except HTTPException:
        return {"status": "ok", "api": "not_configured"}

# ============ Gene Analysis ============

@app.post("/api/analyze")
def analyze_novel(req: AnalyzeRequest):
    """分析小说内容，提取基因（人设、爽点、金句）"""
    try:
        client = get_client()
    except HTTPException as e:
        raise e

    prompt = f"""你是一个资深网文分析师，擅长拆解热门小说的成功要素。

请分析以下小说内容，提取其"成功基因"：

1. 题材类型
2. 人物设定（性格、成长线、金手指）
3. 核心爽点（打脸/逆袭/甜宠/悬疑等）
4. 情绪曲线（前期/中期/高潮）
5. 经典金句（3-5句）

小说内容：
{req.content[:3000]}
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "你是一个资深网文分析师，擅长拆解热门小说的成功要素。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    return {
        "analysis": response.choices[0].message.content,
        "genre": req.genre,
        "model": get_model()
    }

# ============ Story Generation ============

@app.post("/api/generate/story")
def generate_story(req: GenerateStoryRequest):
    """生成小说大纲"""
    try:
        client = get_client()
    except HTTPException as e:
        raise e

    prompt = f"""你是一个专业的小说大纲师，擅长构思吸引人的故事。

请为以下设定生成一个详细的小说大纲：

- 题材：{req.genre}
- 主题：{req.theme}
- 主角：{req.main_char}
- 篇幅：{req.length}

请包含：
1. 世界观设定（1-2段）
2. 主线剧情（3-5个关键节点）
3. 关键转折点（至少2个）
4. 预计章节数
5. 核心爽点设计（3个以上）
6. 主次人物设定（主角+2个配角）
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "你是一个专业的小说大纲师，擅长构思吸引人的故事。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )

    return {
        "outline": response.choices[0].message.content,
        "genre": req.genre,
        "theme": req.theme,
        "length": req.length,
        "model": get_model()
    }

# ============ Chapter Generation ============

@app.post("/api/generate/chapter")
def generate_chapter(req: GenerateChapterRequest):
    """续写章节"""
    try:
        client = get_client()
    except HTTPException as e:
        raise e

    prompt = f"""你是一个网文写手，擅长写节奏快、爽点足的章节。

请根据以下大纲和前文，续写下一章内容：

【大纲】
{req.outline}

【前文】
{req.previous_content[-1500:] if req.previous_content else "（第一章开头）"}

【题材】{req.genre}

要求：
- 字数：约{req.word_count}字
- 保持原有风格
- 节奏明快
- 爽点清晰
- 章节结尾留悬念（钩子）
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"你是一个网文写手，擅长写{req.genre}题材，节奏快、爽点足。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=req.word_count + 500
    )

    return {
        "chapter": response.choices[0].message.content,
        "genre": req.genre,
        "word_count": req.word_count,
        "model": get_model()
    }

# ============ Dialogue Generation ============

@app.post("/api/generate/dialogue")
def generate_dialogue(req: DialogueRequest):
    """生成对话"""
    try:
        client = get_client()
    except HTTPException as e:
        raise e

    emotion_map = {
        "normal": "自然日常",
        "conflict": "剑拔弩张/火药味浓",
        "sweet": "甜蜜暧昧",
        "sad": "悲伤感人",
        "tense": "紧张刺激"
    }

    prompt = f"""请生成{req.character1}和{req.character2}之间的对话：

场景：{req.context}
情感基调：{emotion_map.get(req.emotion, req.emotion)}

要求：
- 符合人物性格
- 推动情节发展
- 字数300-800字
- 对话自然流畅
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "你是一个小说对话写作专家，擅长写生动的对话。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return {
        "dialogue": response.choices[0].message.content,
        "character1": req.character1,
        "character2": req.character2,
        "emotion": req.emotion
    }

# ============ Polish / Refine ============

@app.post("/api/polish")
def polish_chapter(req: PolishRequest):
    """润色章节"""
    try:
        client = get_client()
    except HTTPException as e:
        raise e

    level_map = {
        "light": "轻微润色，保持原汁原味，只改错别字和病句",
        "medium": "中等润色，提升文笔，优化表达，保持原有情节",
        "heavy": "大幅改写，提升爽点和节奏，可适度调整情节"
    }

    prompt = f"""请对以下章节进行{level_map.get(req.level, '中等')}润色：

{req.content}

要求：
- 保持原有情节和人物性格
- 优化表达和节奏
- 提升阅读体验
- 润色后的内容要流畅自然
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "你是一个小说润色专家，擅长提升文笔而不失原味。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=len(req.content) + 500
    )

    return {
        "polished": response.choices[0].message.content,
        "level": req.level
    }

# ============ Gene Library ============

@app.get("/api/genes")
def get_genes(genre: Optional[str] = None):
    """获取基因库（内置模板）"""
    from src.generator.novel import GENRE_GENES

    if genre and genre in GENRE_GENES:
        return {genre: GENRE_GENES[genre]}

    return GENRE_GENES


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
