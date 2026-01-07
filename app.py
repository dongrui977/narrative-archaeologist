import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：Art Deco 风格、黄金勾边、丝绒质感
st.set_page_config(page_title="MindMemo | Golden Palace", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：深翡翠绿丝绒 + 动态金粉纹理 */
    .stApp {
        background-color: #0A1F1C;
        background-image: url("https://www.transparenttextures.com/patterns/dark-matter.png");
        color: #D4AF37; /* 经典复古金 */
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 黄金宫殿入口 */
    .portal-stage {
        display: flex; gap: 40px; justify-content: center; margin-top: 60px;
    }

    .deco-door {
        background: #0D2B26;
        border: 2px solid #D4AF37;
        padding: 60px 30px;
        width: 320px;
        text-align: center;
        position: relative;
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        cursor: pointer;
        /* Art Deco 装饰性金边 */
        box-shadow: 
            inset 0 0 15px rgba(212, 175, 55, 0.5),
            10px 10px 30px rgba(0,0,0,0.5);
    }
    .deco-door:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.8);
        background: #143D36;
    }

    /* 标题：烫金效果 */
    .gold-title {
        font-family: 'Cinzel Decorative', cursive;
        font-size: 2.8rem;
        letter-spacing: 12px;
        text-align: center;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 80px;
        margin-bottom: 10px;
    }

    /* 内容容器：复杂的黄金画框 */
    .golden-frame {
        background: #0D2B26;
        padding: 50px;
        border: 4px double #D4AF37;
        outline: 1px solid #D4AF37;
        outline-offset: 15px;
        position: relative;
        margin-top: 50px;
        box-shadow: 0 50px 100px rgba(0,0,0,0.5);
    }

    /* 按钮：具有物理质感的黄金拨杆 */
    .stButton > button {
        background: linear-gradient(135deg, #BF953F, #AA771C) !important;
        color: #0A1F1C !important;
        border-radius: 0 !important;
        border: 1px solid #FCF6BA !important;
        padding: 15px 0 !important;
        width: 100%;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 700 !important;
        letter-spacing: 4px;
        transition: 0.3s;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .stButton > button:hover {
        filter: brightness(1.2);
        transform: translateY(-2px);
    }

    /* 终极结果：丝绸衬垫上的黄金档案 */
    .final-dossier {
        background: #FDFCF0;
        color: #0A1F1C;
        padding: 60px;
        border: 20px solid #0D2B26;
        outline: 2px solid #D4AF37;
        line-height: 2;
        text-align: left;
    }
    /* 强力修正：所有分析标题对齐 */
    .final-dossier h3 {
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 1.2rem !important;
        color: #AA771C !important;
        border-bottom: 2px solid #AA771C !important;
        padding-bottom: 8px !important;
        margin-top: 35px !important;
        letter-spacing: 3px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话状态
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

# --- 首页：黄金宫殿 ---
if st.session_state.mode is None:
    st.markdown('<div class="gold-title">THE PALACE</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:8px; opacity:0.6; color:#FCF6BA;'>NARRATIVE ARCHAEOLOGY</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            <div class="deco-door">
                <div style="font-size:3rem; margin-bottom:20px; filter:drop-shadow(0 0 10px #D4AF37)">🍮</div>
                <h3 style="font-family:'Cinzel Decorative';">DAILY RELIEF</h3>
                <p style="font-size:0.8rem; opacity:0.7; color:#FCF6BA;">日常情绪清理<br>MindMemo 引擎</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("OPEN DAILY DOOR"):
            st.session_state.mode = 'daily'
            st.rerun()

    with col2:
        st.markdown('''
            <div class="deco-door">
                <div style="font-size:3rem; margin-bottom:20px; filter:drop-shadow(0 0 10px #D4AF37)">🏰</div>
                <h3 style="font-family:'Cinzel Decorative';">DEEP ARCHIVE</h3>
                <p style="font-size:0.8rem; opacity:0.7; color:#FCF6BA;">深度生命考古<br>叙事重构师</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("OPEN DEEP DOOR"):
            st.session_state.mode = 'deep'
            st.rerun()

# --- 日常模式 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown('<div class="golden-frame">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:\"Cinzel Decorative\"; text-align:center;'>MINDMEMO ENGINE</h3>", unsafe_allow_html=True)
    daily_input = st.text_area("", height=200, label_visibility="collapsed", placeholder="请向黄金祭坛倾诉此刻的情绪...")
    
    if st.button("DECODE EMOTION"):
        if daily_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = f"Role: 心理专家。分析：{daily_input}。格式：### 🏷️ 智能标签\\n### 🧠 深度洞察\\n### 🍃 疗愈指引。"
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="final-dossier">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("EXIT PALACE"): 
        st.session_state.mode = None
        st.rerun()

# --- 深度模式 (考古师) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面，以及父母如何在你身上刻下最初的痕迹？"},
        {"icon": "✨", "t": "珠光至暗", "q": "最让你感到荣耀的时刻，以及那个让你至今不敢直视的绝望瞬间？"},
        {"icon": "⚡", "t": "身体警报", "q": "当你压力过载，身体哪个部位会先代替你发出尖叫？"},
        {"icon": "🤝", "t": "重要他人", "q": "谁是你生命中爱恨交织、影响至深的“关键他人”？"},
        {"icon": "🌀", "t": "命运迷宫", "q": "哪个剧本是你发誓不再排练、却一直在重复上演的执念？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f'<div class="golden-frame">', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-family:\"Cinzel Decorative\"; letter-spacing:5px;'>ROOM 0{st.session_state.step + 1}</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:3rem; text-align:center;'>{r['icon']}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center; color:#FCF6BA;'>{r['t']}</h3>", unsafe_allow_html=True)
        st.write(f"**{r['q']}**")
        
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=120)
        if st.button("NEXT ROOM"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
    else:
        if st.button("OPEN DEEP DOSSIER"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = f"Role: 心理考古师。分析数据。极简深刻。格式：### 📜 核心剧本\\n### 🕯️ 觉察时刻\\n### 🍃 行动建议。内容：{' '.join(st.session_state.answers)}"
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="final-dossier">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("RESTART"): 
            st.session_state.mode = None
            st.session_state.step = 0
            st.session_state.answers = []
            st.rerun()
