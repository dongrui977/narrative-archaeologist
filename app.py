import streamlit as st
from openai import OpenAI

# 1. 视觉配置：Art Deco 黄金宫殿 + 紧凑型动态橱窗
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

    /* --- 奇迹橱窗：紧凑型顶部区域 --- */
    .wonder-cabinet {
        height: 120px; /* 进一步缩小高度 */
        width: 100%;
        border: 2px solid #D4AF37;
        margin: 20px 0; /* 调整间距，消除空洞感 */
        position: relative;
        overflow: hidden;
        background: rgba(13, 43, 38, 0.5);
        box-shadow: inset 0 0 20px rgba(212, 175, 55, 0.3);
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    /* 浮动的小物件 */
    .curio {
        font-size: 2.2rem;
        filter: drop-shadow(0 0 8px #D4AF37);
        animation: float-jump 3s infinite ease-in-out;
    }

    @keyframes float-jump {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(8deg); }
    }

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
        font-size: 2.5rem;
        letter-spacing: 10px;
        margin-bottom: 20px;
    }

    .golden-frame {
        background: #0D2B26;
        padding: 30px;
        border: 3px double #D4AF37;
        outline: 1px solid #D4AF37;
        outline-offset: 8px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #BF953F, #AA771C) !important;
        color: #0A1F1C !important;
        border-radius: 0 !important;
        border: 1px solid #FCF6BA !important;
        width: 100%;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 700 !important;
        letter-spacing: 2px;
        padding: 10px 0 !important;
        margin-top: 10px;
    }

    /* 最终报告卡片：强制字号对齐 */
    .final-card {
        background: #FDFCF0;
        color: #1A1A1A;
        padding: 35px;
        border: 12px solid #0D2B26;
        outline: 1px solid #D4AF37;
        line-height: 1.8;
        margin-top: 20px;
    }
    .final-card h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.1rem !important;
        color: #AA771C !important;
        border-bottom: 2px solid #AA771C !important;
        padding-bottom: 5px !important;
        margin-top: 20px !important;
        display: flex;
        align-items: center;
        gap: 10px;
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

# --- 第一幕：入口大厅 ---
if st.session_state.mode is None:
    st.markdown('<h1 class="gold-title">THE PALACE</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="text-align:center; padding:15px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative; font-size:0.9rem;">日常情绪清理</h4><p style="font-size:0.7rem; opacity:0.6; color:#FCF6BA;">MindMemo 引擎</p></div>', unsafe_allow_html=True)
        if st.button("进入日常之门"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div style="text-align:center; padding:15px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative; font-size:0.9rem;">深度生命考古</h4><p style="font-size:0.7rem; opacity:0.6; color:#FCF6BA;">叙事重构师</p></div>', unsafe_allow_html=True)
        if st.button("推开暗室之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 模式 A：日常 ---
elif st.session_state.mode == 'daily':
    st.markdown('<h2 style="text-align:center; font-family:Cinzel Decorative; font-size:1.2rem; margin-bottom:10px;">DAILY CLINIC</h2>', unsafe_allow_html=True)
    st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
    u_input = st.text_area("", height=150, label_visibility="collapsed", placeholder="请向黄金祭坛倾诉此刻的情绪碎片...")
    
    if st.button("生成疗愈档案"):
        if u_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 资深心理咨询师。语气温柔、专业且深刻。极致精简，每项限一句话建议。\n内容：{u_input}\n"
                    f"格式：\n### 🏷️ 智能标签\n### 🧠 深度洞察\n### 🍃 疗愈指引"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("返回大厅 🔄"): reset()

# --- 模式 B：深度 ---
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
        st.markdown(f"<p style='text-align:center; font-family:Cinzel Decorative; font-size:0.8rem;'>ROOM 0{st.session_state.step + 1}</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:2.5rem;'>{r['icon']}</div><h3 style='text-align:center; font-size:1.1rem; color:#FCF6BA;'>{r['t']}</h3><p style='text-align:center; font-size:0.9rem;'>{r['q']}</p>", unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=120, label_visibility="collapsed")
        if st.button("推开下一扇门"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("开启终极档案报告"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 心理专家。语气温柔专业。给出极简、深刻的一句话建议。\n数据：{' '.join(st.session_state.answers)}\n"
                    f"格式：\n### 📜 核心剧本\n### 🎯 觉察时刻\n### 🍃 行动建议"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="final-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("离开宫殿 🔄"): reset()
