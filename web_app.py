"""
Web界面 - Streamlit应用
提供可视化的小说创作界面
"""
import streamlit as st
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator.novel import NovelGenerator, GENRE_GENES
from src.analyzer.gene import GeneAnalyzer
from src.api.minimax_client import MiniMaxClient

# 页面配置
st.set_page_config(
    page_title="AI小说创作助手",
    page_icon="📖",
    layout="wide"
)

# 初始化
if 'generator' not in st.session_state:
    st.session_state.generator = NovelGenerator()

if 'history' not in st.session_state:
    st.session_state.history = []

def main():
    st.title("📖 AI小说创作助手")
    st.markdown("---")
    
    # 侧边栏 - 功能选择
    with st.sidebar:
        st.header("功能导航")
        mode = st.radio(
            "选择功能",
            ["🎯 大纲生成", "✍️ 章节续写", "💬 对话生成", "🔧 章节润色", "🧬 基因分析"]
        )
        
        st.markdown("---")
        st.subheader("📚 题材选择")
        genre = st.selectbox("选择题材", list(GENRE_GENES.keys()))
        st.info(f"核心要素: {', '.join(GENRE_GENES[genre]['elements'][:3])}")
    
    # 主界面
    if mode == "🎯 大纲生成":
        st.header("生成小说大纲")
        
        col1, col2 = st.columns(2)
        with col1:
            theme = st.text_input("主题", placeholder="例如：青春成长")
            main_char = st.text_input("主角", placeholder="例如：张明")
        with col2:
            length = st.selectbox("篇幅", ["短篇", "中篇", "长篇", "超长篇"])
        
        if st.button("生成大纲", type="primary"):
            with st.spinner("AI正在创作中..."):
                result = st.session_state.generator.generate_outline(
                    genre=genre,
                    theme=theme,
                    main_char=main_char,
                    length=length
                )
                st.session_state.current_outline = result
                st.success("生成完成！")
        
        if 'current_outline' in st.session_state:
            st.markdown("### 📝 生成的大纲")
            st.text_area("大纲内容", st.session_state.current_outline["outline"], height=300)
    
    elif mode == "✍️ 章节续写":
        st.header("续写章节")
        
        if 'current_outline' not in st.session_state:
            st.warning("请先生成大纲！")
            return
        
        col1, col2 = st.columns(2)
        with col1:
            chapter_num = st.number_input("章节号", min_value=1, value=1)
            word_count = st.slider("字数", 500, 5000, 2000)
        with col2:
            previous = st.text_area("前文内容（可选）", height=100)
        
        if st.button("续写章节", type="primary"):
            with st.spinner("AI正在续写中..."):
                result = st.session_state.generator.generate_chapter(
                    outline=st.session_state.current_outline["outline"],
                    previous_content=previous,
                    chapter_num=chapter_num,
                    genre=genre,
                    word_count=word_count
                )
                st.session_state.last_chapter = result
                st.success("续写完成！")
        
        if 'last_chapter' in st.session_state:
            st.markdown("### 📝 续写内容")
            st.text_area("章节内容", st.session_state.last_chapter, height=400)
    
    elif mode == "💬 对话生成":
        st.header("生成对话")
        
        col1, col2 = st.columns(2)
        with col1:
            char1 = st.text_input("角色1", placeholder="例如：张三")
            char2 = st.text_input("角色2", placeholder="例如：李四")
        with col2:
            context = st.text_area("场景描述", height=80, placeholder="例如：在咖啡店偶遇")
            emotion = st.selectbox("情感基调", ["normal", "conflict", "sweet", "sad", "tense"],
                                  format_func=lambda x: {"normal": "自然", "conflict": "冲突", "sweet": "甜蜜", "sad": "悲伤", "tense": "紧张"}[x])
        
        if st.button("生成对话", type="primary"):
            with st.spinner("AI正在生成对话..."):
                result = st.session_state.generator.generate_dialogue(
                    character1=char1,
                    character2=char2,
                    context=context,
                    emotion=emotion
                )
                st.session_state.last_dialogue = result
                st.success("生成完成！")
        
        if 'last_dialogue' in st.session_state:
            st.markdown("### 💬 对话内容")
            st.text_area("对话", st.session_state.last_dialogue, height=200)
    
    elif mode == "🔧 章节润色":
        st.header("章节润色")
        
        content = st.text_area("待润色内容", height=300)
        level = st.select_slider("润色强度", ["light", "medium", "heavy"], value="medium",
                                format_func=lambda x: {"light": "轻微", "medium": "中等", "heavy": "大幅"}[x])
        
        if st.button("润色", type="primary"):
            with st.spinner("AI正在润色中..."):
                result = st.session_state.generator.polish_chapter(content, level)
                st.session_state.polished = result
                st.success("润色完成！")
        
        if 'polished' in st.session_state:
            st.markdown("### ✨ 润色结果")
            st.text_area("润色后", st.session_state.polished, height=300)
    
    elif mode == "🧬 基因分析":
        st.header("小说基因分析")
        
        content = st.text_area("待分析内容", height=200, placeholder="粘贴小说内容片段...")
        
        if st.button("分析", type="primary"):
            with st.spinner("AI正在分析中..."):
                # TODO: 连接基因分析模块
                st.info("基因分析功能开发中...")
    
    # 底部 - 历史记录
    st.markdown("---")
    st.subheader("📜 创作历史")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[-5:]):
            st.text(f"{i+1}. {item}")
    else:
        st.info("暂无创作历史")

if __name__ == "__main__":
    main()
