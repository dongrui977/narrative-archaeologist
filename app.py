import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Art Deco 风格 + 动态复古橱窗
st.set_page_config(page_title="MindMemo | 黄金宫殿", layout="centered")

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

    /* --- 奇迹橱窗 (有趣且跳动的顶部区域) --- */
    .wonder-cabinet {
        height: 150px;
        width: 100%;
        border: 2px solid #D4AF37;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        background: rgba(13, 43, 38, 0.5);
        box-shadow: inset 0 0 30px rgba(212, 175, 55, 0.3);
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    /* 浮动的小物件 */
    .curio {
        font-size: 2.8rem;
        filter: drop-shadow(0 0 8px #D4AF37);
        animation: float-jump 3s infinite ease-in-out;
    }

    @keyframes float-jump {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(10deg); }
    }

    /* 差异化动画延迟 */
    .curio:nth-child(1) { animation-delay: 0s; }
    .curio:nth-child(2) { animation-delay: 0.4s; }
    .curio:nth-child(3) { animation-delay: 0.8s; }
    .curio:nth-child(4) { animation-delay: 1.2s; }
    .curio:nth-child(5) { animation-delay: 1.6s; }

    /* --- 核心 UI 样式 --- */
    .gold-title {
        font-family: 'Cinzel Decorative', cursive;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        letter-spacing: 12px;
        margin-bottom: 40px;
    }

    .golden-frame {
        background: #0D2B26;
        padding: 45px;
        border: 4px double #D4AF37;
        outline: 1px solid #D4AF37;
        outline-offset: 10px;
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
        padding: 12px 0 !important;
    }

    /* 最终专业输出卡片 */
    .final-card {
        background: #FDFCF0;
        color: #1A1A1A;
        padding: 45px;
        border: 15px solid #0D2B26;
        outline: 1px solid #D4AF37;
        line-height: 1.8;
    }
    .final-card h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.2rem !important;
        color: #AA771C !important;
        border-bottom: 2px solid #AA771C !important;
        padding-bottom: 8px !important;
        margin-top: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部动态区域 ---
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

# --- 首页 ---
if st.session_state.mode is None:
    st.markdown('<h1 class="gold-title">THE PALACE</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="text-align:center; padding:20px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative;">DAILY RELIEF</h4><p style="font-size:0.7rem; opacity:0.6; color:#FCF6BA;">日常情绪清理</p></div>', unsafe_allow_html=True)
        if st.button("进入日常之门"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div style="text-align:center; padding:20px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative;">DEEP ARCHIVE</h4><p style="font-size:0.7rem; opacity:0.6; color:#FCF6BA;">深度生命考古</p></div>', unsafe_allow_html=True)
        if st.button("推开档案之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 日常模式 ---
elif st.session_state.mode == 'daily':
    st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
    u_input = st.text_area("请在此倾诉...", height=180, label_visibility="collapsed")
    if st.button("生成疗愈建议"):
        if u_input:
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            # 强化专业咨询师语气
            prompt = f"Role: 资深心理咨询师。语气温柔、极致精简、专业深刻。格式：### 🏷️ 智能标签\\n### 🧠 深度洞察\\n### 🍃 疗愈指引。内容：{u_input}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    if st.button("返回"): reset()

# --- 深度模式 ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面？"},
        {"icon": "✨", "t": "珠光至暗", "q": "最荣耀或最绝望的时刻？"},
        {"icon": "⚡", "t": "身体警报", "q": "压力下最先紧绷的部位？"},
        {"icon": "🤝", "t": "重要他人", "q": "影响至深的某个人？"},
        {"icon": "🌀", "t": "循环模式", "q": "不断重复的执念剧本？"}
    ]
    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f'<div class="golden-frame">', unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:3rem;'>{r['icon']}</div><h3 style='text-align:center;'>{r['t']}</h3>", unsafe_allow_html=True)
        ans = st.text_area(r['q'], key=f"d_{st.session_state.step}", height=120)
        if st.button("前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("开启终极简报"):
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            prompt = f"Role: 心理叙事专家。语气专业、温柔。给出极简、深刻的建议。格式：### 📜 核心剧本\\n### 🕯️ 觉察时刻\\n### 🍃 行动指令。数据：{' '.join(st.session_state.answers)}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("离开"): reset()
