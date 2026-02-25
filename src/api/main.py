"""
zhilinainovel - AI小说创作助手
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
from openai import OpenAI

# 配置
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.minimax.chat/v1")
)
MODEL = os.getenv("MODEL", "MiniMax-M2.5")

app = FastAPI(title="zhilinainovel", description="AI小说创作助手")

# ============ 数据模型 ============

class AnalyzeRequest(BaseModel):
    content: str
    genre: Optional[str] = None

class GenerateStoryRequest(BaseModel):
    genre: str
    theme: str
    main_char: str
    length: str = "短篇"  # 短篇/中篇/长篇

class GenerateChapterRequest(BaseModel):
    outline: str
    previous_content: str
    style_genes: Optional[dict] = None

# ============ API 接口 ============

@app.get("/")
def root():
    return {"message": "zhilinainovel API", "version": "0.1.0"}

@app.post("/api/analyze")
def analyze_novel(req: AnalyzeRequest):
    """分析小说内容，提取基因"""
    prompt = f"""请分析以下小说内容，提取其"成功基因"：
    
    1. 题材类型
    2. 人物设定（性格、成长线）
    3. 核心爽点（打脸/逆袭/甜宠/悬疑等）
    4. 情绪曲线（前期/中期/高潮）
    5. 经典金句
    
    小说内容：
    {req.content[:2000]}
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个资深网文分析师，擅长拆解热门小说的成功要素。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "genre": req.genre
    }

@app.post("/api/generate/story")
def generate_story(req: GenerateStoryRequest):
    """生成小说大纲"""
    prompt = f"""请为以下设定生成一个小说大纲：
    
    - 题材：{req.genre}
    - 主题：{req.theme}
    - 主角：{req.main_char}
    - 篇幅：{req.length}
    
    请包含：
    1. 世界观设定
    2. 主线剧情
    3. 关键转折点
    4. 预计章节数
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个专业的小说大纲师，擅长构思吸引人的故事。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    
    return {
        "outline": response.choices[0].message.content,
        "genre": req.genre,
        "length": req.length
    }

@app.post("/api/generate/chapter")
def generate_chapter(req: GenerateChapterRequest):
    """续写章节"""
    prompt = f"""请根据以下大纲和前文，续写下一章内容：
    
    大纲：{req.outline}
    
    前文：{req.previous_content[-1000:]}
    
    要求：
    - 保持原有风格
    - 节奏明快
    - 爽点清晰
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个网文写手，擅长写吸引人的章节。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    
    return {
        "chapter": response.choices[0].message.content
    }

@app.get("/api/genes")
def get_genes(genre: Optional[str] = None):
    """获取基因库"""
    # TODO: 连接数据库获取
    return {
        "message": "基因库功能开发中",
        "genre": genre
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
