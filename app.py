import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Art Deco 黄金宫殿 + 动态复古橱窗
st.set_page_config(page_title="MindMemo | 奇迹宫殿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景 */
    .stApp {
        background-color: #0A1F1C;
        background-image: url("https://www.transparenttextures.com/patterns/dark-matter.png");
        color: #D4AF37;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* --- 奇迹橱窗容器 (有趣的顶部区域) --- */
    .wonder-cabinet {
        height: 180px;
        width: 100%;
        border: 2px solid #D4AF37;
        margin-top: 30px;
        position: relative;
        overflow: hidden;
        background: #0D2B26;
        box-shadow: inset 0 0 30px rgba(212, 175, 55, 0.3);
    }

    /* 装饰性背景线条 */
    .wonder-cabinet::before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: linear-gradient(90deg, rgba(212, 175, 55, 0.1) 1px, transparent 1px);
        background-size: 40px 100%;
    }

    /* 浮动的小玩意：利用 Emoji 模拟复古物件 */
    .curio {
        position: absolute;
        font-size: 2.5rem;
        filter: drop-shadow(0 0 10px #D4AF37);
        animation: curio-jump 4s infinite ease-in-out;
    }

    @keyframes curio-jump {
        0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
        50% { transform: translateY(-40px) rotate(15deg) scale(1.2); }
    }

    /* 不同物件的随机位置和延迟 */
    .curio:nth-child(1) { left: 10%; animation-delay: 0s; }
    .curio:nth-child(2) { left: 25%; animation-delay: 0.5s; font-size: 3rem; }
    .curio:nth-child(3) { left: 45%; animation-delay: 1.2s; }
    .curio:nth-child(4) { left: 65%; animation-delay: 0.8s; font-size: 3.5rem; }
    .curio:nth-child(5) { left: 85%; animation-delay: 1.5s; }

    /* --- 核心 UI 样式 --- */
    .gold-title {
        font-family: 'Cinzel Decorative', cursive;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.2rem;
        letter-spacing: 12px;
        margin: 30px 0;
    }

    .golden-frame {
        background: #0D2B26;
        padding: 50px;
        border: 4px double #D4AF37;
        outline: 1px solid #D4AF37;
        outline-offset: 10px;
        margin-top: 20px;
        box-shadow: 0 50px 100px rgba(0,0,0,0.5);
    }

    .stButton > button {
        background: linear-gradient(135deg, #BF953F, #AA771C) !important;
        color: #0A1F1C !important;
        border-radius: 0 !important;
        border: 1px solid #FCF6BA !important;
        width: 100%;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 700 !important;
        letter-spacing: 3px;
    }

    .final-card {
        background: #FDFCF0;
        color: #0A1F1C;
        padding: 40px;
        border: 12px solid #0D2B26;
        outline: 2px solid #D4AF37;
        line-height: 1.8;
    }
    .final-card h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.3rem !important;
        color: #AA771C !important;
        border-bottom: 2px solid #AA771C !important;
        margin-top: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部动态橱窗 ---
st.markdown('''
    <div class="wonder-cabinet">
        <div class="curio">🏺</div>
        <div class="curio">🍰</div>
        <div class="curio">🕰️</div>
        <div class="curio">✉️</div>
        <div class="curio">✨</div>
    </div>
''', unsafe_allow_html=True)

# 2. 会话逻辑
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

def reset():
    st.session_state.mode = None
    st.session_state.step = 0
    st.session_state.answers = []
    st.rerun()

# --- 第一幕：首页 ---
if st.session_state.mode is None:
    st.markdown('<h1 class="gold-title">THE PALACE</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:8px; color:#FCF6BA; opacity:0.6;'>奇迹档案馆</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("路径 A：日常之门", on_click=lambda: setattr(st.session_state, 'mode', 'daily'))
    with col2:
        st.button("路径 B：暗室之门", on_click=lambda: setattr(st.session_state, 'mode', 'deep'))

# --- 模式 A：日常 ---
elif st.session_state.mode == 'daily':
    st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
    u_input = st.text_area("请在此倾诉...", height=180, label_visibility="collapsed")
    if st.button("开启简报"):
        if u_input:
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            prompt = f"Role: 资深心理咨询师。极简。每项输出限一句话。格式：### 🏷️ 智能标签\\n### 🧠 深度洞察\\n### 🍃 疗愈指引。内容：{u_input}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    if st.button("返回"): reset()

# --- 模式 B：深度 ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面？"},
        {"icon": "✨", "t": "高光至暗", "q": "最让你感到荣耀或绝望的时刻？"},
        {"icon": "⚡", "t": "身体警报", "q": "压力下哪个部位最先紧绷？"},
        {"icon": "🤝", "t": "重要他人", "q": "影响至深的某个人？"},
        {"icon": "🌀", "t": "循环执念", "q": "不断重复的执念模式？"}
    ]
    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f'<div class="golden-frame">', unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:3rem;'>{r['icon']}</div><h3 style='text-align:center;'>{r['t']}</h3>", unsafe_allow_html=True)
        ans = st.text_area(r['q'], key=f"d_{st.session_state.step}", height=120)
        if st.button("前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("开启终极档案"):
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            prompt = f"Role: 叙事重构师。极简、专业、温柔。每项限一句话。格式：### 📜 核心剧本\\n### 🎯 觉察时刻\\n### 🍃 行动建议。内容：{' '.join(st.session_state.answers)}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("离开"): reset()
