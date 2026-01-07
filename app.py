import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：韦斯安德森对称美学 + 极简复古
st.set_page_config(page_title="MindMemo | 心理档案馆", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    .stApp {
        background: #E6E1D6;
        background-image: linear-gradient(rgba(230,225,214,0.85), rgba(230,225,214,0.85)), url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        color: #423629;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 首页入口：绝对对称 */
    .portal-door {
        background: #FDFCF0;
        border: 1px solid #423629;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 10px 10px 0px #423629;
        transition: 0.3s;
    }
    .portal-door:hover { transform: translate(-4px, -4px); box-shadow: 14px 14px 0px #D4A373; }

    /* 电影胶片容器 */
    .film-frame {
        background: #1A1A1A;
        padding: 35px 15px;
        position: relative;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    .film-frame::before, .film-frame::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: #E6E1D6; font-size: 8px; letter-spacing: 18px;
        position: absolute; width: 100%; text-align: center; left: 0;
    }
    .film-frame::before { top: 10px; }
    .film-frame::after { bottom: 10px; }

    .inner-box { background: #FDFCF0; padding: 40px; border: 1px solid #D4A373; }

    /* 按钮：火漆印感 */
    .stButton > button {
        background-color: #423629 !important;
        color: #FDFCF0 !important;
        border: none !important;
        border-radius: 0px !important;
        width: 100%;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 4px;
        box-shadow: 3px 3px 0px #D4A373;
    }

    /* 结果卡片：统一精简格式 */
    .memo-card {
        background: white;
        padding: 40px;
        border: 1px solid #D4A373;
        box-shadow: 0 0 40px rgba(212, 163, 115, 0.2);
        line-height: 1.8;
        font-size: 0.95rem;
    }
    .memo-card h3 { 
        font-family: 'Cinzel', serif; font-size: 1rem; color: #D4A373; 
        border-bottom: 1px solid #eee; padding-bottom: 8px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态逻辑
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
    st.markdown("<h1 style='text-align:center; font-family:Cinzel; letter-spacing:12px; margin-top:60px;'>THE PALACE</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="portal-door"><h3 style="font-family:Cinzel;">DAILY</h3><p style="font-size:0.8rem; opacity:0.6;">此刻情绪清理</p></div>', unsafe_allow_html=True)
        if st.button("进入日常门扉"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div class="portal-door"><h3 style="font-family:Cinzel;">DEEP</h3><p style="font-size:0.8rem; opacity:0.6;">生命档案考古</p></div>', unsafe_allow_html=True)
        if st.button("推开暗室之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 日常模式 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>MINDMEMO</h2>", unsafe_allow_html=True)
    st.markdown('<div class="film-frame"><div class="inner-box"><h4>请倾倒出此刻的情绪碎片。</h4></div></div>', unsafe_allow_html=True)
    
    u_input = st.text_area("", height=150, label_visibility="collapsed", placeholder="输入...")
    if st.button("分析并生成卡片"):
        if u_input:
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            prompt = f"Role: MindMemo引擎。分析以下内容，极简输出。格式：### 🏷️ 标签\\n### 🧠 侦探(CBT)\\n### 🍃 行动(ACT)。内容：{u_input}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="memo-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    if st.button("BACK / 返回大厅"): reset()

# --- 深度模式 (考古师) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面与父母的影响？"},
        {"icon": "✨", "t": "高光至暗", "q": "极度荣耀与极度羞耻的时刻？"},
        {"icon": "💊", "t": "身体记号", "q": "压力大时身体哪个部位先报警？"},
        {"icon": "🤝", "t": "重要他人", "q": "生命中爱恨交织的“关键他人”？"},
        {"icon": "🌀", "t": "循环执念", "q": "发誓不想重复却一直在重复的模式？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f"<p style='text-align:center; font-family:Cinzel;'>ROOM {st.session_state.step+1}/5</p>", unsafe_allow_html=True)
        st.markdown(f'<div class="film-frame"><div class="inner-box"><div style="font-size:2rem;">{r["icon"]}</div><h3 style="font-family:ZCOOL XiaoWei;">{r["t"]}</h3><p>{r["q"]}</p></div></div>', unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=120, label_visibility="collapsed")
        if st.button("PROCEED"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("DECODE / 生成档案"):
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            prompt = f"Role: 心理考古师。分析全量数据，简明扼要。格式：1.【叙事】2.【图式】3.【躯体】4.【情结】5.【觉察】。数据：{' '.join(st.session_state.answers)}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="memo-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        if st.button("EXIT / 离开城堡"): reset()
