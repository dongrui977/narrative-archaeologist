import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：保留 Wes Anderson 对称美学与胶片 UI
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

    /* 首页入口卡片：高级对称 */
    .portal-door {
        background: #FDFCF0;
        border: 1px solid #423629;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 10px 10px 0px #423629;
        transition: 0.3s;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .portal-door:hover { transform: translate(-4px, -4px); box-shadow: 14px 14px 0px #D4A373; }

    /* 电影胶片容器：保留复杂感 */
    .film-frame {
        background: #1A1A1A;
        padding: 45px 15px;
        position: relative;
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .film-frame::before, .film-frame::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: #E6E1D6; font-size: 8px; letter-spacing: 15px;
        position: absolute; width: 100%; text-align: center; left: 0;
    }
    .film-frame::before { top: 15px; }
    .film-frame::after { bottom: 15px; }

    .inner-box { background: #FDFCF0; padding: 40px; border: 1px solid #D4A373; text-align: center; }

    /* 按钮样式 */
    .stButton > button {
        background-color: #423629 !important;
        color: #FDFCF0 !important;
        border: none !important;
        border-radius: 0px !important;
        width: 100%;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 4px;
        box-shadow: 4px 4px 0px #D4A373;
        transition: 0.3s;
    }
    .stButton > button:hover { background-color: #D4A373 !important; color: #1A1A1A !important; }

    /* 结果卡片：保持统一简洁 */
    .memo-card {
        background: #FDFCF0;
        padding: 40px;
        border: 2px solid #423629;
        box-shadow: 0 0 30px rgba(212, 163, 115, 0.2);
        line-height: 1.8;
    }
    .memo-card h3 { 
        font-family: 'Cinzel', serif; font-size: 0.9rem; color: #D4A373; 
        border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态逻辑：确保全循环
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

def restart():
    st.session_state.mode = None
    st.session_state.step = 0
    st.session_state.answers = []
    st.rerun()

# --- 首页：命运之门 ---
if st.session_state.mode is None:
    st.markdown("<h1 style='text-align:center; font-family:Cinzel; letter-spacing:15px; margin-top:60px;'>THE SOUL PALACE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6; letter-spacing:3px; margin-bottom:80px;'>品味生命碎片，或清理当下尘埃</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="portal-door"><div style="font-size:2rem;">🩹</div><h3 style="font-family:Cinzel;">DAILY</h3><p style="font-size:0.7rem; opacity:0.6; letter-spacing:1px;">日常情绪清理</p></div>', unsafe_allow_html=True)
        if st.button("进入日常门扉"): st.session_state.mode = 'daily'; st.rerun()
    with col2:
        st.markdown('<div class="portal-door"><div style="font-size:2rem;">🏺</div><h3 style="font-family:Cinzel;">DEEP</h3><p style="font-size:0.7rem; opacity:0.6; letter-spacing:1px;">生命档案考古</p></div>', unsafe_allow_html=True)
        if st.button("推开暗室之门"): st.session_state.mode = 'deep'; st.rerun()

# --- 模式 A：日常情绪 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>MINDMEMO ENGINE</h2>", unsafe_allow_html=True)
    st.markdown('<div class="film-frame"><div class="inner-box"><h4>请倾倒出此刻的情绪碎片。</h4></div></div>', unsafe_allow_html=True)
    
    daily_input = st.text_area("", height=150, label_visibility="collapsed", placeholder="写下此刻...")
    if st.button("生成分析卡片"):
        if daily_input:
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            # 核心指令：极其简短，去聊天化
            prompt = f"Role: MindMemo。极其简短、深刻、去聊天化。分析以下内容。格式：### 🏷️ 标签\\n### 🧠 侦探(CBT)\\n### 🍃 行动(ACT)。内容：{daily_input}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="memo-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("EXIT / 返回大厅"): restart()

# --- 模式 B：深度考古 (考古师) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面与父母的影响？"},
        {"icon": "✨", "t": "高光至暗", "q": "极度荣耀与极度羞耻的时刻？"},
        {"icon": "💊", "t": "身体记号", "q": "压力大时身体哪个部位先报警？"},
        {"icon": "🤝", "t": "重要他人", "q": "生命中爱恨交织的“关键他人”？"},
        {"icon": "🔀", "t": "循环执念", "q": "发誓不想重复却一直在重复的模式？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f"<p style='text-align:center; font-family:Cinzel; letter-spacing:5px;'>ROOM {st.session_state.step+1}/5</p>", unsafe_allow_html=True)
        st.markdown(f'''<div class="film-frame"><div class="inner-box"><div style="font-size:2.5rem;">{r["icon"]}</div><h3 style="font-family:ZCOOL XiaoWei;">{r["t"]}</h3><h5 style="font-weight:200;">{r["q"]}</h5></div></div>''', unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=120, label_visibility="collapsed")
        if st.button("PROCEED / 下一间"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("DECODE ARCHIVE / 生成档案"):
            client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
            # 核心指令：极其简短，只要揭露，不要建议
            prompt = f"Role: 心理考古师。全量分析，极其简短、冷峻、去聊天化。格式：1.【叙事】2.【图式】3.【躯体】4.【情结】5.【觉察】。数据：{' '.join(st.session_state.answers)}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            st.markdown(f'<div class="memo-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        if st.button("LEAVE / 离开城堡"): restart()
