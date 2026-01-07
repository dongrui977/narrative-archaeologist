import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：香奈儿黑白美学 + 圣光闪烁
st.set_page_config(page_title="MindMemo | Haute Couture", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局：极致黑底 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Noto Serif SC', serif;
    }

    /* 圣光闪烁粒子 */
    .shimmer-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(212, 167, 108, 0.05) 0%, transparent 80%);
        pointer-events: none;
        z-index: 0;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 场景标题：罗马石刻感 */
    .chanel-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        text-align: center;
        letter-spacing: 12px;
        margin-top: 50px;
        color: #d4a76c;
        text-transform: uppercase;
    }

    .chanel-subtitle {
        text-align: center;
        font-size: 0.8rem;
        letter-spacing: 5px;
        opacity: 0.5;
        margin-bottom: 50px;
    }

    /* 输入框：香奈儿极简线条 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid rgba(212, 167, 108, 0.3) !important;
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        text-align: center !important;
        border-radius: 0 !important;
        padding: 30px !important;
        transition: 0.5s;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #d4a76c !important;
        box-shadow: none !important;
    }

    /* 按钮：高定成衣风格 */
    .stButton > button {
        background-color: transparent !important;
        color: #d4a76c !important;
        border: 1px solid #d4a76c !important;
        width: 100%;
        padding: 15px 0 !important;
        letter-spacing: 8px;
        font-family: 'Cinzel', serif;
        transition: 0.8s;
        border-radius: 0px !important;
    }
    .stButton > button:hover {
        background-color: #d4a76c !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(212, 167, 108, 0.4);
    }

    /* 圣光卡片：3:4 黄金比例 + 边缘闪烁 */
    .haute-card {
        background: #FFFFFF;
        color: #000000;
        width: 100%;
        max-width: 450px;
        aspect-ratio: 3 / 4; /* 黄金比例 */
        margin: 50px auto;
        padding: 60px 40px;
        position: relative;
        box-shadow: 0 0 50px rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        justify-content: center;
        animation: cardShimmer 3s infinite alternate;
    }

    @keyframes cardShimmer {
        from { box-shadow: 0 0 20px rgba(212, 167, 108, 0.1); }
        to { box-shadow: 0 0 50px rgba(212, 167, 108, 0.4); }
    }

    .haute-card h3 {
        font-family: 'Cinzel', serif;
        font-size: 1rem;
        color: #000;
        border-bottom: 2px solid #000;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .haute-card p {
        font-size: 0.95rem;
        line-height: 1.8;
        color: #333;
    }
    </style>
    <div class="shimmer-bg"></div>
    """, unsafe_allow_html=True)

# 2. 状态控制
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"title": "The Origin", "sub": "🌱 原生底色"},
    {"title": "The Duality", "sub": "📈 高光与至暗"},
    {"title": "The Echo", "sub": "💊 身体记号"},
    {"title": "The Significant", "sub": "🤝 关键关系"},
    {"title": "The Pattern", "sub": "🔀 转折与执念"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    st.markdown(f'<div class="chanel-title">{s["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chanel-subtitle">{s["sub"]}</div>', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=200, label_visibility="collapsed", placeholder=". . . .")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("PROCEED" if st.session_state.step < 4 else "RECONSTRUCT"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="chanel-title">Finished</div>', unsafe_allow_html=True)
    
    if st.button("OPEN THE ARCHIVE"):
        with st.spinner(""):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                prompt = f"""
                你是一个名为 "MindMemo" 的心理分析引擎。
                任务：生成一张极其简短、深刻的“心理卡片”。
                分析内容：{full_context}
                
                输出格式：
                ### 🏷️ 智能标签
                ### 🧠 思维侦探 (CBT)
                ### 🍃 接纳与行动 (ACT)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                # 圣光闪烁卡片显示
                st.markdown(f'''
                    <div class="haute-card">
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                # 循环逻辑
                if st.button("REWATCH"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
                    
            except Exception as e:
                st.error("API Error.")
