import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：莫兰迪高级感 + 浮雕微拟物 (Neumorphism)
st.set_page_config(page_title="MindMemo | Soul Cabinet", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Noto+Serif+SC:wght@200;400&display=swap');

    /* 全局背景：高级暖灰色绸缎感 */
    .stApp {
        background-color: #E5E5E5;
        background-image: linear-gradient(180deg, #E5E5E5 0%, #D8D8D8 100%);
        color: #4A4A4A;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 浮雕质感的中央面板 */
    .cabinet-stage {
        background: #E5E5E5;
        border-radius: 4px;
        padding: 60px 40px;
        box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
        text-align: center;
        margin-top: 50px;
        border: 1px solid rgba(255,255,255,0.3);
    }

    .cabinet-label {
        font-family: 'Cinzel', serif;
        font-size: 0.75rem;
        letter-spacing: 6px;
        color: #A68E6B; /* 香槟金 */
        margin-bottom: 25px;
        display: block;
    }

    .cabinet-title {
        font-size: 1.8rem;
        font-weight: 400;
        color: #2D2D2D;
        margin-bottom: 40px;
        letter-spacing: 2px;
    }

    /* 极致纤细的输入框：像在精密纸张上刻字 */
    .stTextArea textarea {
        background: transparent !important;
        border: none !important;
        border-bottom: 1px solid #C4C4C4 !important;
        color: #2D2D2D !important;
        font-size: 1.1rem !important;
        border-radius: 0 !important;
        padding: 20px 0 !important;
        transition: 0.5s;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #A68E6B !important;
        box-shadow: none !important;
    }

    /* 按钮：具有物理质感的“拨杆” */
    .stButton > button {
        background: #E5E5E5 !important;
        color: #4A4A4A !important;
        border-radius: 50px !important;
        border: 1px solid #D1D1D1 !important;
        padding: 10px 50px !important;
        font-family: 'Cinzel', serif;
        letter-spacing: 4px;
        font-size: 0.8rem !important;
        box-shadow: 6px 6px 12px #bebebe, -6px -6px 12px #ffffff;
        transition: 0.2s;
        margin-top: 40px;
    }
    .stButton > button:active {
        box-shadow: inset 4px 4px 8px #bebebe, inset -4px -4px 8px #ffffff;
        transform: scale(0.98);
    }

    /* 珍珠母贝质感的分析卡片 */
    .pearl-card {
        background: #FDFDFD;
        padding: 60px 45px;
        border-radius: 2px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.1);
        text-align: left;
        position: relative;
        overflow: hidden;
        animation: pearlGlow 4s infinite alternate;
    }
    @keyframes pearlGlow {
        0% { box-shadow: 0 0 30px rgba(166, 142, 107, 0.1); }
        100% { box-shadow: 0 0 60px rgba(166, 142, 107, 0.3); }
    }
    .pearl-card h3 {
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        color: #A68E6B;
        border-bottom: 1px solid #EEE;
        padding-bottom: 12px;
        margin-top: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态控制
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"label": "I. THE ORIGIN", "title": "🌱 原生底色"},
    {"label": "II. THE RADIANCE", "title": "✨ 闪光时刻"},
    {"label": "III. THE ABYSS", "title": "🌑 至暗瞬间"},
    {"label": "IV. THE ECHO", "title": "🌡️ 身体警报"},
    {"label": "V. THE MIRROR", "title": "🤝 重要他人"},
    {"label": "VI. THE SCRIPT", "title": "🌀 循环怪圈"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="cabinet-stage">
            <span class="cabinet-label">{s['label']}</span>
            <div class="cabinet-title">{s['title']}</div>
            <p style="color: #999; font-size: 0.8rem; letter-spacing: 2px;">COLLECTING MEMORY COMPONENT</p>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=180, label_visibility="collapsed", placeholder="请如实刻录...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("NEXT COMPONENT"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="cabinet-title" style="text-align:center; margin-top:100px; color:#A68E6B;">COLLECTION COMPLETE</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("DECODE ARCHIVE"):
            with st.spinner(""):
                try:
                    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                    full_context = "\n".join(st.session_state.answers)
                    
                    prompt = f"""
                    你是一个名为 "MindMemo" 的心理分析引擎。
                    任务：生成极其简短、冷峻且深刻的“心理卡片”。
                    分析视角：ACT + CBT。不要建议，只要揭露。
                    输入：{full_context}
                    格式：
                    ### 🏷️ 灵魂标签
                    ### 🧠 脚本监测 (CBT)
                    ### 🍃 进化路径 (ACT)
                    """
                    
                    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                    
                    st.markdown(f'''
                        <div class="pearl-card">
                            <div style="text-align:center; font-family:Cinzel; letter-spacing:5px; color:#A68E6B; margin-bottom:30px;">MINDMEMO DOSSIER</div>
                            {response.choices[0].message.content}
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    if st.button("RESTART ARCHIVE"):
                        st.session_state.step = 0
                        st.session_state.answers = []
                        st.rerun()
                        
                except Exception as e:
                    st.error("Engine Error.")
