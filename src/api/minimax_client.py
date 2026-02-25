"""
MiniMax 优化客户端
充分利用 Coding Plus 套餐
"""
from openai import OpenAI
import os
from typing import List, Dict, Optional
import time

class MiniMaxClient:
    """MiniMax API 优化客户端"""
    
    # 推荐模型配置
    MODELS = {
        "code": "kimi-code/kimi-for-codi",      # 代码生成
        "reason": "kimi-code/kimi-for-codi",   # 推理
        "fast": "MiniMax-M2.5",                 # 快速对话
        "long": "MiniMax-Text-01",              # 长文本（200K上下文）
        "default": "MiniMax-M2.5"                # 默认
    }
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.minimax.chat/v1")
        )
        self.default_model = os.getenv("MODEL", self.MODELS["default"])
    
    def chat(
        self, 
        messages: List[Dict], 
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs
    ):
        """优化的对话接口"""
        model = model or self.default_model
        
        # 自动选择最优模型
        if "代码" in str(messages) or "code" in str(messages).lower():
            model = self.MODELS["code"]
        
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs
        )
    
    def code_review(self, code: str, language: str = "python") -> str:
        """代码审查"""
        messages = [
            {"role": "system", "content": "你是一个资深代码审查专家。"},
            {"role": "user", "content": f"请审查以下{language}代码，指出问题并给出优化建议：\n\n```{language}\n{code}\n```"}
        ]
        return self.chat(messages, model=self.MODELS["code"]).choices[0].message.content
    
    def generate_story(
        self, 
        genre: str, 
        theme: str, 
        chapters: int = 3,
        style_genes: Dict = None
    ) -> str:
        """小说生成（zhilinainovel核心功能）"""
        gene_context = ""
        if style_genes:
            gene_context = f"\n\n参考基因：{style_genes}"
        
        messages = [
            {"role": "system", "content": f"你是一个专业的小说作家，擅长写{genre}题材。"},
            {"role": "user", "content": f"请创作一个关于"{theme}"的{genre}小说，要求：\n1. {chapters}章以上\n2. 人物丰满、情节曲折{gene_context}"}
        ]
        return self.chat(messages, model=self.MODELS["fast"], max_tokens=8192).choices[0].message.content
    
    def analyze_content(self, content: str, analysis_type: str = "gene") -> str:
        """内容分析"""
        prompts = {
            "gene": "分析以下内容，提取成功基因（人设、爽点、金句）",
            "summary": "为以下内容生成简洁摘要",
            "outline": "为以下内容生成大纲"
        }
        
        messages = [
            {"role": "system", "content": "你是一个专业的的内容分析师。"},
            {"role": "user", "content": f"{prompts.get(analysis_type, '分析')}：\n\n{content[:5000]}"}
        ]
        
        return self.chat(messages, model=self.MODELS["fast"]).choices[0].message.content
    
    def batch_process(self, tasks: List[Dict], delay: float = 0.5) -> List[str]:
        """批量处理任务"""
        results = []
        for task in tasks:
            result = self.chat(
                messages=task.get("messages", []),
                model=task.get("model", self.default_model)
            ).choices[0].message.content
            results.append(result)
            time.sleep(delay)  # 避免触发速率限制
        return results


# 便捷函数
def get_client() -> MiniMaxClient:
    """获取优化后的客户端"""
    return MiniMaxClient()


if __name__ == "__main__":
    client = get_client()
    print("MiniMax 优化客户端就绪")
    print(f"默认模型: {client.default_model}")
