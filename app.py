import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Art Deco 繁复美学 + 动态居中橱窗
st.set_page_config(page_title="MindMemo | 终极宫殿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Noto+Serif+SC:wght@200;500;900&display=swap');

    /* 全局背景：深翡翠丝绒 */
    .stApp {
        background-color: #0A1F1C;
        background-image: radial-gradient(circle at 50% 50%, rgba(20, 61, 54, 0.8) 0%, #0A1F1C 100%),
            url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #D4AF37;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* --- 动态奇迹橱窗 (居中对齐版) --- */
    .wonder-cabinet {
        height: 140px;
        width: 100%;
        border: 1px solid #D4AF37;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        background: rgba(13, 43, 38, 0.6);
        box-shadow: inset 0 0 50px rgba(212, 175, 55, 0.3), 0 0 0 6px #0A1F1C, 0 0 0 8px #D4AF37;
        
        /* 强制居中对齐 */
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 0 20px;
    }

    .cabinet-deco {
        position: absolute;
        width: 100%; height: 100%;
        background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(212, 175, 55, 0.05) 40px, rgba(212, 175, 55, 0.05) 41px);
        pointer-events: none;
    }

    .curio {
        font-size: 2.8rem;
        filter: drop-shadow(0 0 12px #D4AF37);
        animation: curio-float 4s infinite cubic-bezier(0.45, 0.05, 0.55, 0.95);
        position: relative; /* 脱离绝对定位，交由 Flex 布局 */
    }
    
    @keyframes curio-float {
        0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.8; }
        50% { transform: translateY(-20px) rotate(8deg); opacity: 1; }
    }

    .curio:nth-child(2) { animation-delay: 0.5s; }
    .curio:nth-child(3) { animation-delay: 1s; }
    .curio:nth-child(4) { animation-delay: 1.5s; }
    .curio:nth-child(5) { animation-delay: 2s; }

    /* --- 核心 UI 样式 --- */
    .gold-title {
        font-family: 'Cinzel Decorative', cursive;
        background: linear-gradient(to bottom, #FCF6BA 0%, #BF953F 50%, #FCF6BA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        letter-spacing: 12px;
        margin-bottom: 30px;
        font-weight: 900;
    }

    .golden-frame {
        background: #0D2B26;
        padding: 40px;
        border: 2px solid #D4AF37;
        position: relative;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
        margin-top: 10px;
    }

    /* 按钮：具有物理质感的烫金 */
    .stButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #8A6E2F 100%) !important;
        color: #0A1F1C !important;
        border: 1px solid #FCF6BA !important;
        border-radius: 0 !important;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 900 !important;
        letter-spacing: 3px;
        height: 55px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.1);
    }

    /* 报告卡片：高级咨询室纸质感 */
    .report-card {
        background: #FDFCF0;
        color: #1A1A1A;
        padding: 45px;
        border: 15px solid #0D2B26;
        outline: 1px solid #D4AF37;
        line-height: 2;
        margin-top: 25px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
    }
    .report-card h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.2rem !important;
        color: #8A6E2F !important;
        border-bottom: 2px solid #D4AF37 !important;
        padding-bottom: 10px !important;
        margin-top: 25px !important;
        font-weight: 900 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 顶部：动态奇迹橱窗 ---
st.markdown('''
    <div class="wonder-cabinet">
        <div class="cabinet-deco"></div>
        <div class="curio">🏺</div>
        <div class="curio">🕰️</div>
        <div class="curio">🍰</div>
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

# --- 第一幕：入口 ---
if st.session_state.mode is None:
    st.markdown('<div class="gold-title">THE PALACE</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="text-align:center; padding:25px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative;">DAILY RELIEF</h4><p style="font-size:0.75rem; opacity:0.6; color:#FCF6BA;">此刻情绪清理</p></div>', unsafe_allow_html=True)
        if st.button("进入日常之门"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div style="text-align:center; padding:25px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative;">DEEP ARCHIVE</h4><p style="font-size:0.75rem; opacity:0.6; color:#FCF6BA;">深度考古之旅</p></div>', unsafe_allow_html=True)
        if st.button("推开档案之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 模式 A：日常情绪 (专业咨询师视角) ---
elif st.session_state.mode == 'daily':
    st.markdown("<h3 style='text-align:center; font-family:Cinzel Decorative; letter-spacing:4px;'>DAILY CLINIC</h3>", unsafe_allow_html=True)
    u_input = st.text_area("", height=200, label_visibility="collapsed", placeholder="请在此处倾诉，无需顾虑逻辑...")
    
    if st.button("生成专家疗愈档案"):
        if u_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                # 提示词强化：专业、深刻、一句话建议
                prompt = (
                    f"Role: 临床心理咨询师。语气专业、克制且极具洞察力。去聊天化。\n"
                    f"要求：每项仅限一句话。给出能够点破本质的分析。\n"
                    f"内容：{u_input}\n"
                    f"格式：\n### 🏷️ 核心防御\n### 🧠 潜意识映射\n### 🍃 临床建议"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("EXIT / 返回大厅"): reset()

# --- 模式 B：深度考古 (叙事重构师视角) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的一个画面？父母如何塑造了早期的你？"},
        {"icon": "✨", "t": "珠光至暗", "q": "最让你感到荣耀的时刻，以及那个让你至今难以释怀的瞬间？"},
        {"icon": "⚡", "t": "身体警报", "q": "当你压力过载，身体哪个部位会最先代替你发出尖叫？"},
        {"icon": "🤝", "t": "重要他人", "q": "谁是你生命中爱恨交织、影响至深的“关键他人”？"},
        {"icon": "🌀", "t": "循环模式", "q": "你发现自己在不断重复上演的某种不快乐的人生剧本？"}
    ]
    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f'<div class="golden-frame"><div style="text-align:center; font-size:3.5rem;">{r["icon"]}</div><h3 style="text-align:center;">{r["t"]}</h3><p style="text-align:center; color:#FCF6BA; font-weight:200;">{r["q"]}</p>', unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=120, label_visibility="collapsed")
        if st.button("PROCEED / 前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("GENERATE CLINICAL REPORT / 开启报告"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 叙事重构师/临床专家。语气冷峻、专业、深刻。每项仅限一句话建议。\n"
                    f"数据：{' '.join(st.session_state.answers)}\n"
                    f"格式：\n### 📜 核心剧本\n### 🎯 觉察瞬间\n### 🍃 重构指引"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("EXIT / 离开"): reset()
