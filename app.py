import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Art Deco 黄金宫殿风格
st.set_page_config(page_title="MindMemo | 黄金宫殿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：深翡翠绿丝绒 */
    .stApp {
        background-color: #0A1F1C;
        background-image: url("https://www.transparenttextures.com/patterns/dark-matter.png");
        color: #D4AF37;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 黄金宫殿入口 */
    .portal-door {
        background: #0D2B26;
        border: 2px solid #D4AF37;
        padding: 50px 30px;
        text-align: center;
        box-shadow: inset 0 0 15px rgba(212, 175, 55, 0.5), 10px 10px 30px rgba(0,0,0,0.5);
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .portal-door:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.8);
    }

    /* 烫金标题 */
    .gold-title {
        font-family: 'Cinzel Decorative', cursive;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 60px;
    }

    /* 黄金画框内容区 */
    .golden-frame {
        background: #0D2B26;
        padding: 50px;
        border: 4px double #D4AF37;
        outline: 1px solid #D4AF37;
        outline-offset: 10px;
        margin-top: 40px;
        box-shadow: 0 50px 100px rgba(0,0,0,0.5);
    }

    /* 按钮：具有物理质感的黄金 */
    .stButton > button {
        background: linear-gradient(135deg, #BF953F, #AA771C) !important;
        color: #0A1F1C !important;
        border-radius: 0 !important;
        border: 1px solid #FCF6BA !important;
        width: 100%;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 700 !important;
        letter-spacing: 3px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    /* 最终简报卡片：强制字号对齐 */
    .final-card {
        background: #FDFCF0;
        color: #0A1F1C;
        padding: 50px;
        border: 15px solid #0D2B26;
        outline: 1px solid #D4AF37;
        line-height: 2;
    }
    .final-card h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.3rem !important;
        color: #AA771C !important;
        border-bottom: 2px solid #AA771C !important;
        padding-bottom: 8px !important;
        margin-top: 30px !important;
        display: flex !important;
        align-items: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话逻辑
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

def reset():
    st.session_state.mode = None
    st.session_state.step = 0
    st.session_state.answers = []
    st.rerun()

# --- 首页 ---
if st.session_state.mode is None:
    st.markdown('<h1 class="gold-title" style="font-size:3rem; letter-spacing:10px;">THE PALACE</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:5px; color:#FCF6BA; opacity:0.6;'>灵魂档案馆</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="portal-door"><div style="font-size:2.5rem;">🩹</div><h3 style="font-family:Cinzel Decorative;">DAILY RELIEF</h3><p style="font-size:0.75rem; color:#FCF6BA;">日常情绪清理<br>MindMemo 引擎</p></div>', unsafe_allow_html=True)
        if st.button("进入日常之门"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div class="portal-door"><div style="font-size:2.5rem;">🏺</div><h3 style="font-family:Cinzel Decorative;">DEEP ARCHIVE</h3><p style="font-size:0.75rem; color:#FCF6BA;">深度生命考古<br>叙事重构师</p></div>', unsafe_allow_html=True)
        if st.button("推开暗室之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 日常模式 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-family:Cinzel Decorative;'>DAILY CLINIC</h2>", unsafe_allow_html=True)
    u_input = st.text_area("", height=200, label_visibility="collapsed", placeholder="请在此倾诉此刻的情绪碎片...")
    
    if st.button("生成档案"):
        if u_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 资深心理咨询师。语气温柔且言简意赅。每项输出限一句话。\n内容：{u_input}\n"
                    f"格式：\n### 🏷️ 智能标签\n### 🧠 深度洞察\n### 🍃 疗愈指引"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("BACK / 返回大厅"): reset()

# --- 深度模式 (考古师) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的一个画面？父母如何潜移默化地塑造了你？"},
        {"icon": "✨", "t": "高光至暗", "q": "最让你感到荣耀的时刻，以及那个最想逃避的绝望瞬间？"},
        {"icon": "⚡", "t": "身体警报", "q": "压力过载时，你的身体哪个部位会最先感到紧绷或疼痛？"},
        {"icon": "🤝", "t": "重要他人", "q": "生命中对你影响至深的某个人，无论你爱他还是恨他？"},
        {"icon": "🌀", "t": "循环执念", "q": "哪种不快乐的相处模式，是你发现自己在不断重复的？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f'<div class="golden-frame"><p style="text-align:center; font-family:Cinzel Decorative;">ROOM 0{st.session_state.step + 1}</p>', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:3rem; text-align:center;'>{r['icon']}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center; color:#FCF6BA;'>{r['t']}</h3><p style='text-align:center;'>{r['q']}</p>", unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=150, label_visibility="collapsed")
        if st.button("PROCEED / 前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("DECODE / 开启档案"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 心理叙事重构师/咨询师。语气温柔、极致精简、专业深刻。每项仅限一句话。\n"
                    f"数据：{' '.join(st.session_state.answers)}\n"
                    f"格式：\n### 📜 核心剧本\n### 🎯 觉察时刻\n### 🍃 行动建议"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("EXIT / 离开"): reset()
