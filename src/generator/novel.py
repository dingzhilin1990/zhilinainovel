"""
小说创作引擎 - 核心生成模块
支持多题材、多风格、自动书写
"""
from typing import Dict, List, Optional
import json
from src.api.minimax_client import MiniMaxClient

# 题材基因库
GENRE_GENES = {
    "玄幻": {
        "elements": ["修炼体系", "功法", "灵宠", "异火", "阵法", "境界划分"],
        "excitement": ["越级挑战", "宝物现世", "势力崛起", "境界突破", "传承觉醒"],
        "structure": "升级流",
        "keywords": ["穿越", "系统", "退婚", "废柴", "系统"]
    },
    "都市": {
        "elements": ["职场", "豪门", "风水", "医术", "商战", "炒股"],
        "excitement": ["打脸", "甜宠", "逆袭", "马甲", "神豪"],
        "structure": "生活流",
        "keywords": ["总裁", "赘婿", "神医", "兵王", "复仇"]
    },
    "悬疑": {
        "elements": ["推理", "线索", "密室", "不在场证明", "反转", "心理"],
        "excitement": ["解密", "紧张", "推理", "真相大白", "细思极恐"],
        "structure": "悬念流",
        "keywords": ["盗墓", "灵异", "破案", "心理咨询师"]
    },
    "科幻": {
        "elements": ["星际", "机甲", "基因", "AI", "末世", "系统"],
        "excitement": ["科技突破", "文明战争", "人类进化", "维度跃迁"],
        "structure": "设定流",
        "keywords": ["星际", "末世", "系统", "AI", "游戏"]
    },
    "言情": {
        "elements": ["甜宠", "虐恋", "双向", "暗恋", "豪门"],
        "excitement": ["甜蜜", "误会", "解谜", "告白", "求婚"],
        "structure": "情感流",
        "keywords": ["甜文", "虐文", "校园", "职场", "闪婚"]
    },
    "历史": {
        "elements": ["朝堂", "战争", "谋略", "经商", "科举"],
        "excitement": ["权谋", "战争", "逆袭", "发明", "改革"],
        "structure": "历史流",
        "keywords": ["穿越", "架空", "争霸", "科举", "经商"]
    }
}

class NovelGenerator:
    """AI小说自动生成引擎"""
    
    def __init__(self, client: MiniMaxClient = None):
        self.client = client or MiniMaxClient()
    
    def generate_outline(
        self,
        genre: str,
        theme: str,
        main_char: str,
        length: str = "短篇",
        style_genes: Dict = None
    ) -> Dict:
        """生成小说大纲"""
        gene_info = GENRE_GENES.get(genre, GENRE_GENES["都市"])
        
        prompt = f"""你是一个专业的小说大纲师。请为以下设定生成详细大纲：

## 基本设定
- 题材：{genre}
- 主题：{theme}
- 主角：{main_char}
- 篇幅：{length}

## {genre}题材基因
- 核心要素：{', '.join(gene_info['elements'])}
- 常见爽点：{', '.join(gene_info['excitement'])}
- 结构模式：{gene_info['structure']}

{f"## 参考风格基因：{json.dumps(style_genes, ensure_ascii=False)}" if style_genes else ""}

请生成：
1. 世界观设定（1-2句话）
2. 主线剧情（3-5个关键节点）
3. 主次人物设定（主角+2-3个配角）
4. 预计章节数
5. 核心爽点设计"""

        result = self.client.chat(
            messages=[
                {"role": "system", "content": "你是一个专业的小说大纲师，擅长构思吸引人的故事。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        
        return {
            "genre": genre,
            "theme": theme,
            "outline": result.choices[0].message.content,
            "chapters": self._estimate_chapters(length)
        }
    
    def generate_chapter(
        self,
        outline: str,
        previous_content: str,
        chapter_num: int,
        genre: str = "都市",
        style_genes: Dict = None,
        word_count: int = 2000
    ) -> str:
        """续写章节"""
        gene_info = GENRE_GENES.get(genre, GENRE_GENES["都市"])
        
        prompt = f"""请根据以下大纲，续写第{chapter_num}章内容：

## 大纲
{outline}

## 前文摘要
{previous_content[-500:] if previous_content else "（开头）"}

## 题材要求
- 题材：{genre}
- 核心要素：{', '.join(gene_info['elements'])}
- 爽点：{', '.join(gene_info['excitement'])}

{f"## 风格基因：{json.dumps(style_genes, ensure_ascii=False)}" if style_genes else ""}

要求：
- 字数：约{word_count}字
- 保持原有风格
- 节奏明快
- 爽点清晰
- 章节结尾留悬念"""

        result = self.client.chat(
            messages=[
                {"role": "system", "content": f"你是一个网文写手，擅长写{genre}题材，节奏快、爽点足。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=word_count + 500
        )
        
        return result.choices[0].message.content
    
    def generate_dialogue(
        self,
        character1: str,
        character2: str,
        context: str,
        emotion: str = "normal"
    ) -> str:
        """生成对话"""
        emotion_map = {
            "normal": "自然日常",
            "conflict": "剑拔弩张",
            "sweet": "甜蜜暧昧",
            "sad": "悲伤感人",
            "tense": "紧张刺激"
        }
        
        prompt = f"""请生成{character1}和{character2}之间的对话：

## 场景
{context}

## 情感基调
{emotion_map.get(emotion, emotion)}

要求：
- 符合人物性格
- 推动情节发展
- 字数200-500字"""

        result = self.client.chat(
            messages=[
                {"role": "system", "content": "你是一个小说对话写作专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        
        return result.choices[0].message.content
    
    def generate_scene(
        self,
        location: str,
        time: str,
        mood: str,
        key_events: List[str]
    ) -> str:
        """生成场景描写"""
        prompt = f"""请描写以下场景：

- 地点：{location}
- 时间：{time}
- 氛围：{mood}
- 关键事件：{', '.join(key_events)}

要求：
- 画面感强
- 渲染氛围
- 字数300-800字"""

        result = self.client.chat(
            messages=[
                {"role": "system", "content": "你是一个小说场景描写专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        return result.choices[0].message.content
    
    def polish_chapter(self, content: str, level: str = "medium") -> str:
        """润色章节"""
        level_desc = {
            "light": "轻微润色，保持原汁原味",
            "medium": "中等润色，提升文笔",
            "heavy": "大幅改写，提升爽点"
        }
        
        prompt = f"""请对以下章节进行{level_desc.get(level, level)}：

{content}

要求：
- 保持原有情节
- 优化表达
- 提升阅读体验"""

        result = self.client.chat(
            messages=[
                {"role": "system", "content": "你是一个小说润色专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=len(content) + 500
        )
        
        return result.choices[0].message.content
    
    def _estimate_chapters(self, length: str) -> int:
        """估算章节数"""
        return {
            "短篇": 10,
            "中篇": 30,
            "长篇": 100,
            "超长篇": 300
        }.get(length, 10)


def get_generator() -> NovelGenerator:
    """获取生成器实例"""
    return NovelGenerator()


if __name__ == "__main__":
    gen = get_generator()
    
    # 测试大纲生成
    outline = gen.generate_outline("都市", "逆袭", "张明")
    print("=== 大纲 ===")
    print(outline["outline"])
