import streamlit as st
from openai import OpenAI

# 1. 强制注入顶级视觉样式
st.set_page_config(page_title="生命叙事档案馆", page_icon="🎞️", layout="centered")

st.markdown("""
    <style>
    /* 全局背景：彻底黑场 */
    .stApp {
        background-color: #050505;
        color: #C19A6B; /* 经典的琥珀金 */
    }

    /* 隐藏所有系统 UI */
    header, footer, #MainMenu {visibility: hidden;}

    /* 营造电影独白感 */
    .movie-frame {
        padding: 100px 20px;
        text-align: center;
        animation: fadeIn 3s ease-in;
    }

    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }

    .question-text {
        font-family: 'STSong', 'SimSun', serif; /* 使用衬线体更有质感 */
        font-size: 1.8rem;
        letter-spacing: 0.2rem;
        line-height: 1.6;
        margin-bottom: 60px;
        text-shadow: 0 0 15px rgba(193, 154, 107, 0.4);
    }

    /* 极简输入框：去掉灰色背景，只留底线 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid rgba(193, 154, 107, 0.3) !important;
        color: #F5F5F5 !important;
        font-size: 1.3rem !important;
        text-align: center !important;
        border-radius: 0 !important;
    }
    
    .stTextArea textarea:focus {
        border-bottom: 1px solid rgba(193, 154, 107, 0.8) !important;
        box-shadow: none !important;
    }

    /* 电影“下一幕”按钮 */
    .stButton > button {
        background-color: transparent !important;
        color: rgba(193, 154, 107, 0.6) !important;
        border: 1px solid rgba(193, 154, 107, 0.3) !important;
        padding: 10px 40px !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3rem !important;
        transition: 0.5s;
        margin-top: 40px;
    }

    .stButton > button:hover {
        color: #C19A6B !important;
        border-color: #C19A6B !important;
        background-color: rgba(193, 154, 107, 0.05) !important;
    }

    /* 结果框 */
    .report-box {
        border-left: 1px solid #C19A6B;
        padding: 40px;
        font-style: italic;
        line-height: 2.2;
        font-size: 1.1rem;
        color: rgba(245, 245, 245, 0.9);
        background: linear-gradient(90deg, rgba(193, 154, 107, 0.05), transparent);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 逻辑控制
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

questions = [
    "那一秒，你觉得自己在这世界上是真实的。",
    "如果另一个你留在了原地，他现在会是什么样子？",
    "关上房门的那一刻，第一个浮现的念头。",
    "他们眼中的你，和你心中的你，隔着多远的距离？",
    "如果不考虑明天，这个周末你想消失在哪里？"
]

# 3. API 初始化
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

# --- 场景渲染 ---
if st.session_state.step < len(questions):
    st.markdown(f'<div class="movie-frame">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{questions[st.session_state.step]}</div>', unsafe_allow_html=True)
    
    ans = st.text_area("", placeholder=". . . . . .", key=f"in_{st.session_state.step}", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        label = "封 存" if st.session_state.step == 4 else "接 下 来"
        if st.button(label):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 报告生成 ---
else:
    st.markdown('<div class="movie-frame"><div class="question-text">记忆正在发酵 . . .</div>', unsafe_allow_html=True)
    
    if st.button("打 开 档 案"):
        with st.spinner(""):
            all_ans = st.session_state.answers
            prompt = f"王家卫风格。基于这些生命碎片：{all_ans}。写一段200字旁白，解读此人的生命底色。用第三人称，破碎、诗意、冷峻。"
            
            response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="report-box">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
            
            if st.button("重 启"):
                st.session_state.step = 0
                st.session_state.answers = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
