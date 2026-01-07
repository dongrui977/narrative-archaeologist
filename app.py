import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：3D 景深、电影滤镜、强制对齐
st.set_page_config(page_title="MindMemo Palace", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局：复古电影滤镜 */
    .stApp {
        background: #E6E1D6;
        background-image: 
            linear-gradient(rgba(230,225,214,0.8), rgba(230,225,214,0.8)),
            url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        color: #423629;
        font-family: 'Noto Serif SC', serif;
        perspective: 1200px; /* 增加 3D 纵深 */
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 宫殿大门入口 */
    .portal-stage {
        display: flex; gap: 40px; justify-content: center; margin-top: 60px;
    }

    .mendl-door {
        background: #FDFCF0;
        border: 1px solid #423629;
        padding: 60px 30px;
        width: 320px;
        text-align: center;
        box-shadow: 20px 20px 0px rgba(66, 54, 41, 0.15);
        transition: 0.6s cubic-bezier(0.19, 1, 0.22, 1);
        cursor: pointer;
        position: relative;
    }
    .mendl-door:hover {
        transform: translateZ(50px) rotateY(-10deg);
        box-shadow: 30px 30px 60px rgba(0,0,0,0.2);
        border-color: #D4A373;
    }

    /* 电影胶片转场框架 */
    .film-vault {
        background: #1A1A1A;
        padding: 50px 20px;
        border-radius: 2px;
        position: relative;
        box-shadow: 0 50px 100px rgba(0,0,0,0.4);
        animation: slideIn 1s ease-out;
    }
    @keyframes slideIn {
        from { transform: rotateX(20deg) translateY(100px); opacity: 0; }
        to { transform: rotateX(0deg) translateY(0); opacity: 1; }
    }

    .film-vault::before, .film-vault::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: rgba(230, 225, 214, 0.4); font-size: 8px; letter-spacing: 16px;
        position: absolute; width: 100%; text-align: center; left: 0;
    }
    .film-vault::before { top: 15px; }
    .film-vault::after { bottom: 15px; }

    .paper-sheet {
        background: #FDFCF0;
        padding: 50px;
        border: 1px solid #D4A373;
        min-height: 400px;
    }

    /* 高级火漆印按钮 */
    .stButton > button {
        background: #423629 !important;
        color: #FDFCF0 !important;
        border-radius: 0 !important;
        border: none !important;
        padding: 15px 0 !important;
        width: 100%;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 5px;
        box-shadow: 5px 5px 0px #D4A373;
        transition: 0.3s;
    }
    .stButton > button:active { transform: translate(3px, 3px); box-shadow: none; }

    /* 终极结果卡片：强制对齐所有标题 */
    .dossier-card {
        background: white;
        padding: 60px;
        border: 1px solid #423629;
        box-shadow: 0 0 80px rgba(212, 163, 115, 0.25);
        line-height: 2;
        text-align: left;
    }
    .dossier-card h3 {
        font-family: 'Cinzel', serif !important;
        font-size: 1.4rem !important; /* 强制所有标题对齐 */
        font-weight: 700 !important;
        color: #A68E6B !important; /* 香槟金标题 */
        border-bottom: 2px solid #F4EBE2;
        padding-bottom: 10px;
        margin-top: 35px !important;
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话逻辑 (全闭环)
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

def exit_to_hall():
    st.session_state.mode = None
    st.session_state.step = 0
    st.session_state.answers = []
    st.rerun()

# --- 第一幕：宫殿大厅 ---
if st.session_state.mode is None:
    st.markdown("<h1 style='text-align:center; font-family:Cinzel; letter-spacing:15px; margin-top:80px;'>THE PALACE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.5; letter-spacing:5px;'>NARRATIVE ARCHAEOLOGY & DAILY RELIEF</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="mendl-door"><h3>🍮</h3><h4 style="font-family:Cinzel;">Daily Relief</h4><p style="font-size:0.8rem; opacity:0.6;">此刻情绪清理</p></div>', unsafe_allow_html=True)
        if st.button("进入日常门扉"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div class="mendl-door"><h3>🏰</h3><h4 style="font-family:Cinzel;">Deep Archive</h4><p style="font-size:0.8rem; opacity:0.6;">生命档案考古</p></div>', unsafe_allow_html=True)
        if st.button("推开暗室之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 第二幕：日常处理 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>MINDMEMO</h2>", unsafe_allow_html=True)
    st.markdown('<div class="film-vault"><div class="paper-sheet"><h4>此刻，请倾倒出堆积的情绪碎片。</h4><p style="opacity:0.4; font-size:0.8rem;">ENGINE IS STANDING BY...</p></div></div>', unsafe_allow_html=True)
    
    u_input = st.text_area("", height=180, label_visibility="collapsed", placeholder="随意书写，无需逻辑...")
    
    if st.button("执行静默分析"):
        if u_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                # 提示词增加“极简格式”与“标题空格”指令，确保对齐
                prompt = f"Role: MindMemo。专业心理咨询师，极其简短、深刻。格式：### 🏷️ 智能标签\\n### 🧠 思维侦探 (CBT)\\n### 🍃 接纳建议 (ACT)。内容：{u_input}"
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="dossier-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("EXIT / 离开"): exit_to_hall()

# --- 第三幕：深度模式 (叙事重构) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面，以及父母如何在你身上刻下最初的痕迹？"},
        {"icon": "✨", "t": "珠光至暗", "q": "最让你感到荣耀的时刻，以及那个让你至今不敢直视的绝望瞬间？"},
        {"icon": "⚡", "t": "身体警报", "q": "当你压力过载，身体哪个部位会先代替你发出尖叫？"},
        {"icon": "🤝", "title": "重要他人", "q": "谁是你生命中爱恨交织、影响至深的“关键他人”？"},
        {"icon": "🌀", "title": "命运迷宫", "q": "哪个不爽的剧本，是你发誓不再排练却一直在重复上演的？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f"<p style='text-align:center; font-family:Cinzel; letter-spacing:8px;'>ROOM 0{st.session_state.step + 1}</p>", unsafe_allow_html=True)
        st.markdown(f'''<div class="film-vault"><div class="paper-sheet"><div style="font-size:3rem; margin-bottom:20px;">{r["icon"]}</div><h3 style="font-family:ZCOOL XiaoWei;">{r["t"]}</h3><p style="font-size:1.1rem;">{r["q"]}</p></div></div>''', unsafe_allow_html=True)
        
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=120, label_visibility="collapsed")
        if st.button("PROCEED / 前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("DECODE ARCHIVE / 开启档案"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
    f"Role: 心理考古师\n"
    f"要求：专业心理咨询师，去聊天化，冷峻深刻。不要分析过程，直接给出灵魂洞察。每项限一句话。\n"
    f"数据：{' '.join(st.session_state.answers)}\n"
    f"格式：\n"
    f"### 🎯 核心剧本\n(一句话定性你的底层逻辑)\n\n"
    f"### 🕯️ 觉察之光\n(一句话点破你的核心执念)\n\n"
    f"### 🍃 行动指令\n(一个立刻去做的具体建议)"
)
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="dossier-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        if st.button("EXIT / 离开城堡"): exit_to_hall()
