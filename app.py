import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Art Deco 繁复美学 + 动态金线 + 浮雕质感
st.set_page_config(page_title="The Palace | 黄金档案馆", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Noto+Serif+SC:wght@200;500;900&display=swap');

    /* 全局：深翡翠丝绒背景 */
    .stApp {
        background-color: #0A1F1C;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(20, 61, 54, 0.8) 0%, #0A1F1C 100%),
            url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #D4AF37;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* --- 极致 Fancy：动态奇迹橱窗 --- */
    .wonder-cabinet {
        height: 160px;
        width: 100%;
        border: 1px solid #D4AF37;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        background: rgba(13, 43, 38, 0.6);
        /* 几何金边装饰层 */
        box-shadow: 
            inset 0 0 50px rgba(212, 175, 55, 0.3),
            0 0 0 6px #0A1F1C,
            0 0 0 8px #D4AF37;
    }

    /* 装饰：几何射线条纹 */
    .cabinet-deco {
        position: absolute;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(212, 175, 55, 0.05) 40px, rgba(212, 175, 55, 0.05) 41px);
        pointer-events: none;
    }

    /* 浮动物件：物理震颤感 */
    .curio {
        position: absolute;
        font-size: 2.8rem;
        filter: drop-shadow(0 0 15px #D4AF37);
        animation: curio-float 4s infinite cubic-bezier(0.45, 0.05, 0.55, 0.95);
    }
    @keyframes curio-float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); opacity: 0.8; }
        33% { transform: translate(5px, -25px) rotate(5deg); opacity: 1; }
        66% { transform: translate(-5px, -15px) rotate(-5deg); opacity: 0.9; }
    }

    /* --- 核心 UI：精密机械感 --- */
    .gold-title {
        font-family: 'Cinzel Decorative', cursive;
        background: linear-gradient(to bottom, #FCF6BA 0%, #BF953F 25%, #8A6E2F 50%, #BF953F 75%, #FCF6BA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        letter-spacing: 15px;
        font-weight: 900;
        text-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }

    /* 黄金框架：三层嵌套结构 */
    .golden-frame {
        background: #0D2B26;
        padding: 40px;
        border: 2px solid #D4AF37;
        position: relative;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }
    .golden-frame::before {
        content: ""; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px;
        border: 1px solid rgba(212, 175, 55, 0.3); pointer-events: none;
    }

    /* 按钮：烫金浮雕效果 */
    .stButton > button {
        background: linear-gradient(180deg, #D4AF37 0%, #8A6E2F 100%) !important;
        color: #0A1F1C !important;
        border: 1px solid #FCF6BA !important;
        border-radius: 0 !important;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 900 !important;
        letter-spacing: 4px;
        height: 55px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.4), inset 0 2px 5px rgba(255,255,255,0.5);
        transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1);
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.4);
    }

    /* 结果报告：特种纸质感 */
    .report-card {
        background: #FDFCF0;
        color: #1A1A1A;
        padding: 50px;
        border: 20px solid #0D2B26;
        outline: 1px solid #D4AF37;
        line-height: 2.2;
        box-shadow: 0 50px 100px rgba(0,0,0,0.5);
    }
    .report-card h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.25rem !important;
        color: #8A6E2F !important;
        border-bottom: 2px solid #D4AF37 !important;
        padding-bottom: 10px !important;
        margin-top: 30px !important;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 首页：动态奇迹橱窗 ---
st.markdown('''
    <div class="wonder-cabinet">
        <div class="cabinet-deco"></div>
        <div class="curio" style="left:10%;">🏺</div>
        <div class="curio" style="left:30%; animation-delay:0.5s;">🕰️</div>
        <div class="curio" style="left:50%; animation-delay:1.2s;">🍰</div>
        <div class="curio" style="left:70%; animation-delay:0.8s;">✉️</div>
        <div class="curio" style="left:90%; animation-delay:1.5s;">✨</div>
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
    st.markdown('<div class="gold-title">THE PALACE</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:8px; color:#FCF6BA; opacity:0.8; font-weight:200;'>灵魂叙事与情绪考古</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="text-align:center; padding:30px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative;">DAILY RELIEF</h4><p style="font-size:0.7rem; color:#FCF6BA; opacity:0.6;">此刻情绪清理</p></div>', unsafe_allow_html=True)
        if st.button("进入日常之门"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div style="text-align:center; padding:30px; border:1px solid #D4AF37; background:#0D2B26;"><h4 style="font-family:Cinzel Decorative;">DEEP ARCHIVE</h4><p style="font-size:0.7rem; color:#FCF6BA; opacity:0.6;">深度考古之旅</p></div>', unsafe_allow_html=True)
        if st.button("推开档案之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 模式 A：日常情绪 ---
elif st.session_state.mode == 'daily':
    st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-family:Cinzel Decorative; letter-spacing:5px;'>MIND ENGINE</h2>", unsafe_allow_html=True)
    u_input = st.text_area("", height=220, label_visibility="collapsed", placeholder="向黄金祭坛倾诉...")
    
    if st.button("生成疗愈简报"):
        if u_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                # AI 指令：极简专家视角
                prompt = (
                    f"Role: 资深心理咨询师。语气冷峻而温柔，直击灵魂。\n"
                    f"要求：去聊天化，每项仅限一句话。给出极具实操性的洞察。\n"
                    f"内容：{u_input}\n"
                    f"格式：\n### 🏷️ 智能标签\n### 🧠 深度洞察\n### 🍃 疗愈指引"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("EXIT / 返回大厅 🔄"): reset()

# --- 模式 B：深度考古 ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面？"},
        {"icon": "✨", "t": "珠光至暗", "q": "最荣耀或最绝望的时刻？"},
        {"icon": "⚡", "t": "身体警报", "q": "压力下最先紧绷的部位？"},
        {"icon": "🤝", "t": "重要他人", "q": "生命中爱恨交织的某个人？"},
        {"icon": "🌀", "t": "循环模式", "q": "重复上演的执念剧本？"}
    ]
    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-family:Cinzel Decorative; opacity:0.5;'>ROOM 0{st.session_state.step + 1}</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:3.5rem; filter:drop-shadow(0 0 10px #D4AF37);'>{r['icon']}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center; letter-spacing:3px;'>{r['t']}</h3><p style='text-align:center; font-weight:200;'>{r['q']}</p>", unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=140, label_visibility="collapsed")
        if st.button("PROCEED / 前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("OPEN THE DOSSIER / 开启档案"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 心理考古师。专业、温柔、深刻。极简输出，每项限一句话。\n"
                    f"数据：{' '.join(st.session_state.answers)}\n"
                    f"格式：\n### 📜 核心剧本\n### 🎯 觉察时刻\n### 🍃 行动指令"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="report-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("LEAVE / 离开 🔄"): reset()
