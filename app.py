import streamlit as st
from openai import OpenAI

# 1. 视觉工程：Tiffany 蓝 + 极简高级感
st.set_page_config(page_title="MindMemo | Tiffany Edition", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@200;500&family=Cinzel&display=swap');

    /* 全局背景：Tiffany 经典色 */
    .stApp {
        background-color: #81D8D0;
        background-image: linear-gradient(135deg, #81D8D0 0%, #AEE6E1 100%);
        color: #333;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 高级白盒容器 */
    .tiffany-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 2px; /* 珠宝盒通常是方正的 */
        padding: 60px 40px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 50px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .tiffany-label {
        font-family: 'Cinzel', serif;
        font-size: 0.8rem;
        letter-spacing: 5px;
        color: #81D8D0;
        margin-bottom: 20px;
        font-weight: bold;
    }

    .tiffany-title {
        font-size: 1.8rem;
        font-weight: 200;
        color: #1a1a1a;
        margin-bottom: 40px;
        letter-spacing: 2px;
    }

    /* 输入框：极细线条 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #eee !important;
        color: #1a1a1a !important;
        font-size: 1.1rem !important;
        border-radius: 0 !important;
        padding: 20px 0 !important;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #81D8D0 !important;
        box-shadow: none !important;
    }

    /* 按钮：深蓝色绸缎感 */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: white !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 12px 60px !important;
        font-size: 0.8rem !important;
        letter-spacing: 4px;
        transition: 0.5s;
        margin-top: 30px;
    }
    .stButton > button:hover {
        background-color: #333 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
    }

    /* 圣光珠宝卡片 */
    .jewelry-card {
        background: white;
        padding: 50px;
        border: 1px solid #eee;
        text-align: left;
        position: relative;
        animation: moonGlow 3s infinite alternate;
    }
    @keyframes moonGlow {
        from { box-shadow: 0 0 20px rgba(255,255,255,0.5); }
        to { box-shadow: 0 0 50px rgba(129, 216, 208, 0.4); }
    }

    .jewelry-card h3 {
        font-family: 'Cinzel', serif;
        font-size: 1rem;
        color: #81D8D0;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-top: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"label": "01 THE ORIGIN", "title": "🌱 原生底色"},
    {"label": "02 THE LIGHT", "title": "✨ 闪光时刻"},
    {"label": "03 THE SHADOW", "title": "🌑 至暗瞬间"},
    {"label": "04 THE ECHO", "title": "🌡️ 身体警报"},
    {"label": "05 THE CONNECTION", "title": "🤝 重要他人"},
    {"label": "06 THE REPETITION", "title": "🌀 循环怪圈"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="tiffany-container">
            <div class="tiffany-label">{s['label']}</div>
            <div class="tiffany-title">{s['title']}</div>
            <p style="color: #999; font-size: 0.9rem;">第 {st.session_state.step + 1} 帧 / 共 6 帧</p>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=180, label_visibility="collapsed", placeholder="记录您的真实叙事...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("PROCEED"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="tiffany-title" style="text-align:center; margin-top:100px; color:white;">ARCHIVE COMPLETE</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("OPEN THE BLUE BOX"):
            with st.spinner(""):
                try:
                    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                    full_context = "\n".join(st.session_state.answers)
                    
                    prompt = f"""
                    你是一个名为 "MindMemo" 的心理分析引擎。
                    任务：生成极其简短深刻的“心理卡片”。
                    分析视角：ACT + CBT。
                    输入：{full_context}
                    格式：
                    ### 🏷️ 智能标签
                    ### 🧠 思维侦探 (CBT)
                    ### 🍃 接纳与行动 (ACT)
                    """
                    
                    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                    
                    st.markdown(f'''
                        <div class="jewelry-card">
                            <div style="text-align:center; font-family:Cinzel; letter-spacing:3px; color:#81D8D0; margin-bottom:20px;">MINDMEMO ARCHIVE</div>
                            {response.choices[0].message.content}
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    if st.button("RESTART JOURNEY"):
                        st.session_state.step = 0
                        st.session_state.answers = []
                        st.rerun()
                        
                except Exception as e:
                    st.error("Connection Error.")
