"""
AI 小说创作助手
"""
import os
from openai import OpenAI

# 配置API
_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your .env file or export it before running."
    )

client = OpenAI(
    api_key=_api_key,
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.minimax.chat/v1")
)

def generate_story(genre: str, prompt: str, max_tokens: int = 1000) -> str:
    """生成小说内容"""
    response = client.chat.completions.create(
        model=os.getenv("MODEL", "MiniMax-M2.5"),
        messages=[
            {"role": "system", "content": f"你是一个专业的小说作家，擅长写{genre}题材"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # 示例
    story = generate_story("都市", "写一个关于青春成长的故事开头")
    print(story)
