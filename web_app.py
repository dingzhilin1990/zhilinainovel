"""
zhilinainovel - Streamlit Web UI
AI小说创作助手 - 可视化界面
"""

import streamlit as st
import sys
import os

# Add project root to path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.generator.novel import NovelGenerator, GENRE_GENES
from src.analyzer.gene import GeneAnalyzer
from src.api.minimax_client import MiniMaxClient

# Page config
st.set_page_config(
    page_title="AI小说创作助手",
    page_icon="📖",
    layout="wide"
)

# ============ API Client Setup ============

def get_api_client() -> MiniMaxClient:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("MINIMAX_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.minimax.chat/v1")
    return MiniMaxClient(api_key=api_key, base_url=base_url)

def get_model() -> str:
    return os.getenv("MODEL", "MiniMax-M2.5")

# ============ Session State Init ============

if 'generator' not in st.session_state:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("MINIMAX_API_KEY")
    if api_key:
        try:
            st.session_state.generator = NovelGenerator()
            st.session_state.api_ready = True
        except Exception as e:
            st.session_state.api_ready = False
            st.session_state.api_error = str(e)
    else:
        st.session_state.api_ready = False

if 'history' not in st.session_state:
    st.session_state.history = []

# ============ Sidebar ============

with st.sidebar:
    st.header("📚 AI小说创作助手")
    st.markdown("---")

    # API status
    if st.session_state.get('api_ready', False):
        st.success("✅ API 已连接")
        st.caption(f"模型: {get_model()}")
    else:
        st.warning("⚠️ API 未配置")
        st.markdown("""
        请设置环境变量：
        ```bash
        export OPENAI_API_KEY=your-key
        export OPENAI_BASE_URL=https://api.minimax.chat/v1
        export MODEL=MiniMax-M2.5
        ```
        或在 Streamlit 中通过 secrets 配置。
        """)

    st.markdown("---")
    st.subheader("🎯 功能导航")
    mode = st.radio(
        "选择功能",
        [
            "🎯 大纲生成",
            "✍️ 章节续写",
            "💬 对话生成",
            "🔧 章节润色",
            "🧬 基因分析",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.subheader("📚 题材选择")
    genre = st.selectbox("题材", list(GENRE_GENES.keys()), label_visibility="collapsed")
    st.caption(f"要素: {', '.join(GENRE_GENES[genre]['elements'][:3])}")

    st.markdown("---")
    if st.button("🗑️ 清空历史", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ============ Main Area ============

st.title("📖 AI小说创作助手")

if not st.session_state.get('api_ready', False):
    st.error("请先配置 API Key 才能使用。设置环境变量后重启应用。")
    st.stop()

# ---- 大纲生成 ----
if mode == "🎯 大纲生成":
    st.header("生成小说大纲")

    col1, col2 = st.columns(2)
    with col1:
        theme = st.text_input("小说主题", placeholder="例如：逆袭成长", label_visibility="collapsed")
        main_char = st.text_input("主角姓名", placeholder="例如：张明", label_visibility="collapsed")
    with col2:
        length = st.selectbox("篇幅", ["短篇", "中篇", "长篇", "超长篇"])
        genre_choice = st.selectbox("题材", list(GENRE_GENES.keys()))

    col_start = st.columns(1)[0]
    with col_start:
        if st.button("🚀 生成大纲", type="primary", use_container_width=True):
            if not theme:
                st.warning("请输入小说主题")
            elif not main_char:
                st.warning("请输入主角姓名")
            else:
                with st.spinner("AI正在构思中..."):
                    try:
                        result = st.session_state.generator.generate_outline(
                            genre=genre_choice,
                            theme=theme,
                            main_char=main_char,
                            length=length
                        )
                        st.session_state.current_outline = result
                        st.session_state.history.append({
                            "type": "大纲",
                            "genre": genre_choice,
                            "theme": theme,
                            "char": main_char,
                            "length": length
                        })
                        st.success("✅ 大纲生成完成！")
                    except Exception as e:
                        st.error(f"生成失败: {e}")

    if 'current_outline' in st.session_state:
        st.markdown("### 📝 生成的大纲")
        st.text_area(
            "大纲内容",
            st.session_state.current_outline.get("outline", ""),
            height=350,
            label_visibility="collapsed"
        )

        # Download button
        outline_text = st.session_state.current_outline.get("outline", "")
        st.download_button(
            "📥 下载大纲",
            outline_text,
            file_name=f"大纲_{st.session_state.current_outline.get('genre', '都市')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ---- 章节续写 ----
elif mode == "✍️ 章节续写":
    st.header("续写章节")

    if 'current_outline' not in st.session_state:
        st.info("💡 建议先在「大纲生成」中创建大纲，再来这里续写章节。")

    col1, col2 = st.columns(2)
    with col1:
        chapter_num = st.number_input("章节号", min_value=1, value=1, step=1)
        word_count = st.slider("目标字数", 500, 5000, 2000, step=100)
    with col2:
        previous = st.text_area(
            "前文内容（最近1-2章）",
            value=st.session_state.get('last_chapter', ''),
            height=100,
            placeholder="粘贴前文内容，帮助 AI 保持上下文一致...",
            label_visibility="collapsed"
        )

    if st.button("✍️ 续写章节", type="primary", use_container_width=True):
        if 'current_outline' not in st.session_state:
            st.warning("请先在大纲生成中创建大纲！")
        else:
            with st.spinner("AI正在创作中，请稍候..."):
                try:
                    result = st.session_state.generator.generate_chapter(
                        outline=st.session_state.current_outline.get("outline", ""),
                        previous_content=previous,
                        chapter_num=chapter_num,
                        genre=st.session_state.current_outline.get("genre", "都市"),
                        word_count=word_count
                    )
                    st.session_state.last_chapter = result
                    st.session_state.history.append({
                        "type": "章节",
                        "chapter": chapter_num,
                        "words": word_count
                    })
                    st.success("✅ 章节续写完成！")
                except Exception as e:
                    st.error(f"续写失败: {e}")

    if st.session_state.get('last_chapter'):
        st.markdown("### 📝 续写内容")
        st.text_area(
            "章节内容",
            st.session_state.last_chapter,
            height=400,
            label_visibility="collapsed"
        )
        st.download_button(
            "📥 下载章节",
            st.session_state.last_chapter,
            file_name=f"第{st.session_state.get('chapter_num', 1)}章.txt",
            mime="text/plain",
            use_container_width=True
        )

# ---- 对话生成 ----
elif mode == "💬 对话生成":
    st.header("生成对话")

    col1, col2 = st.columns(2)
    with col1:
        char1 = st.text_input("角色1", placeholder="例如：张三")
        char2 = st.text_input("角色2", placeholder="例如：李四")
    with col2:
        context = st.text_area("场景描述", height=80, placeholder="例如：咖啡店偶遇，两人曾是恋人")
        emotion = st.selectbox(
            "情感基调",
            ["normal", "conflict", "sweet", "sad", "tense"],
            format_func=lambda x: {
                "normal": "😊 自然",
                "conflict": "😤 冲突",
                "sweet": "😍 甜蜜",
                "sad": "😢 悲伤",
                "tense": "😰 紧张"
            }[x]
        )

    if st.button("💬 生成对话", type="primary", use_container_width=True):
        if not char1 or not char2:
            st.warning("请输入两个角色姓名")
        else:
            with st.spinner("AI正在生成对话..."):
                try:
                    result = st.session_state.generator.generate_dialogue(
                        character1=char1,
                        character2=char2,
                        context=context,
                        emotion=emotion
                    )
                    st.session_state.last_dialogue = result
                    st.success("✅ 对话生成完成！")
                except Exception as e:
                    st.error(f"生成失败: {e}")

    if st.session_state.get('last_dialogue'):
        st.markdown("### 💬 对话内容")
        st.text_area("对话", st.session_state.last_dialogue, height=250, label_visibility="collapsed")

# ---- 章节润色 ----
elif mode == "🔧 章节润色":
    st.header("章节润色")

    content = st.text_area("待润色内容", height=280, placeholder="粘贴需要润色的章节内容...")
    level = st.select_slider(
        "润色强度",
        ["light", "medium", "heavy"],
        value="medium",
        format_func=lambda x: {
            "light": "🌿 轻微（保持原味）",
            "medium": "🌳 中等（提升文笔）",
            "heavy": "🔥 大幅（强化爽点）",
        }[x]
    )

    if st.button("🔧 开始润色", type="primary", use_container_width=True):
        if not content:
            st.warning("请输入需要润色的内容")
        else:
            with st.spinner("AI正在润色中..."):
                try:
                    result = st.session_state.generator.polish_chapter(content, level)
                    st.session_state.polished = result
                    st.success("✅ 润色完成！")
                except Exception as e:
                    st.error(f"润色失败: {e}")

    if st.session_state.get('polished'):
        st.markdown("### ✨ 润色结果")
        st.text_area("润色后", st.session_state.polished, height=280, label_visibility="collapsed")
        st.caption(f"字数变化: {len(content)} → {len(st.session_state.polished)}")

# ---- 基因分析 ----
elif mode == "🧬 基因分析":
    st.header("小说基因分析")

    st.info("💡 粘贴一段小说内容，AI 将分析其成功基因（人设、爽点、金句）")

    content = st.text_area("待分析内容", height=200, placeholder="粘贴小说内容片段（建议300字以上）...")
    analyze_genre = st.selectbox("指定题材（可选）", ["自动判断"] + list(GENRE_GENES.keys()))

    if st.button("🔬 分析基因", type="primary", use_container_width=True):
        if len(content) < 100:
            st.warning("内容太少，建议至少粘贴300字以上")
        else:
            with st.spinner("AI正在分析中..."):
                try:
                    client = get_api_client()
                    genre_param = None if analyze_genre == "自动判断" else analyze_genre

                    prompt = f"""你是一个资深网文分析师，擅长拆解热门小说的成功要素。

请分析以下小说内容，提取其"成功基因"：

1. 题材类型（判断依据）
2. 人物设定（性格、成长线、金手指）
3. 核心爽点（按类型分类：打脸/逆袭/甜宠/悬疑等）
4. 情绪曲线（前期/中期/高潮的节奏特点）
5. 经典金句（3-5句）
6. 写作风格特点

小说内容：
{content[:4000]}
"""

                    response = client.chat(
                        messages=[
                            {"role": "system", "content": "你是一个资深网文分析师，擅长拆解热门小说的成功要素。"},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=2000
                    )

                    st.session_state.gene_analysis = response.choices[0].message.content
                    st.success("✅ 分析完成！")
                except Exception as e:
                    st.error(f"分析失败: {e}")

    if st.session_state.get('gene_analysis'):
        st.markdown("### 🧬 基因分析结果")
        st.markdown(st.session_state.gene_analysis)

# ============ Footer: History ============

st.markdown("---")
st.subheader("📜 创作历史")
if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history[-10:])):
        st.text(f"• {item.get('type', '?')}: {item}")
else:
    st.caption("暂无创作历史")
