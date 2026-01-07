import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：高定诊所质感 + 绝对对称美学
st.set_page_config(page_title="MindMemo | 心理档案馆", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：复古亚麻纸张质感 */
    .stApp {
        background: #E6E1D6;
        background-image: linear-gradient(rgba(230,225,214,0.85), rgba(230,225,214,0.85)), 
            url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        color: #4A4036;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 首页入口：像两扇通往内心的厚重木门 */
    .portal-door {
        background: #FDFCF0;
        border: 1px solid #4A4036;
        padding: 50px 30px;
        text-align: center;
        box-shadow: 12px 12px 0px #4A4036;
        transition: 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .portal-door:hover {
        transform: translateY(-8px);
        box-shadow: 18px 18px 0px #D4A373;
        border-color: #D4A373;
    }

    /* 电影胶片转场框架 */
    .film-frame {
        background: #1A1A1A;
        padding: 45px 20px;
        border-radius: 2px;
        position: relative;
        box-shadow: 0 40px 80px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }
    .film-frame::before, .film-frame::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: #E6E1D6; font-size: 8px; letter-spacing: 16px;
        position: absolute; width: 100%; text-align: center; left: 0;
    }
    .film-frame::before { top: 15px; }
    .film-frame::after { bottom: 15px; }

    .inner-box {
        background: #FDFCF0;
        padding: 40px;
        border: 1px solid #D4A373;
        text-align: center;
    }

    /* 按钮样式：火漆印章质感 */
    .stButton > button {
        background-color: #4A4036 !important;
        color: #FDFCF0 !important;
        border: none !important;
        border-radius: 0px !important;
        width: 100%;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 5px;
        font-size: 0.9rem !important;
        padding: 15px 0 !important;
        box-shadow: 4px 4px 0px #D4A373;
        transition: 0.3s;
    }
    .stButton > button:hover { background-color: #D4A373 !important; color: #1A1A1A !important; }

    /* 最终结果卡片：强制对齐字号 */
    .memo-card {
        background: white;
        padding: 50px;
        border: 1px solid #D4A373;
        box-shadow: 0 0 50px rgba(212, 163, 115, 0.2);
        line-height: 2;
        text-align: left;
    }
    /* 强制所有 ### 标题字号一致 */
    .memo-card h3 {
        font-family: 'Cinzel', serif !important;
        font-size: 1.3rem !important; 
        font-weight: 600 !important;
        color: #D4A373 !important;
        border-bottom: 1px solid #F5EFE6;
        padding-bottom: 10px;
        margin-top: 30px !important;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态逻辑：完美循环
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

def reset():
    st.session_state.mode = None
    st.session_state.step = 0
    st.session_state.answers = []
    st.rerun()

# --- 第一幕：城堡入口 ---
if st.session_state.mode is None:
    st.markdown("<h1 style='text-align:center; font-family:Cinzel; letter-spacing:15px; margin-top:50px;'>THE SOUL PALACE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:3px; opacity:0.6; margin-bottom:80px;'>品味生命，或清理尘埃</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            <div class="portal-door">
                <div style="font-size:3rem; margin-bottom:20px;">🍮</div>
                <h3 style="font-family:Cinzel;">DAILY RELIEF</h3>
                <p style="font-size:0.8rem; opacity:0.7;">日常情绪清理<br>MindMemo 引擎</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("进入日常门扉"):
            st.session_state.mode = 'daily'
            st.rerun()

    with col2:
        st.markdown('''
            <div class="portal-door">
                <div style="font-size:3rem; margin-bottom:20px;">🏰</div>
                <h3 style="font-family:Cinzel;">DEEP ARCHIVE</h3>
                <p style="font-size:0.8rem; opacity:0.7;">深度生命考古<br>叙事重构师</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("推开档案暗室"):
            st.session_state.mode = 'deep'
            st.rerun()

# --- 模式 A：日常情绪 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>DAILY CLINIC</h2>", unsafe_allow_html=True)
    st.markdown('<div class="film-frame"><div class="inner-box"><h4>请倾倒出此刻的情绪碎片。</h4><p style="font-size:0.8rem; opacity:0.4;">引擎将为您生成专业疗愈建议</p></div></div>', unsafe_allow_html=True)
    
    u_input = st.text_area("", height=180, label_visibility="collapsed", placeholder="随意书写，无需逻辑...")
    if st.button("执行静默分析"):
        if u_input:
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 专业心理咨询师\n要求：语气温柔、坚定且专业。禁止废话。针对输入给出核心洞察与行动建议。\n内容：{u_input}\n"
                    f"格式：\n### 🏷️ 智能标签\n(2个词)\n\n### 🧠 深度洞察\n(一句话点破本质)\n\n### 🍃 疗愈指引\n(一个温柔有效的具体行动建议)"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="memo-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("EXIT / 离开"): reset()

# --- 模式 B：深度考古 (考古师) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "t": "原生底色", "q": "童年记忆中最深刻的画面，以及父母如何在你身上刻下最初的痕迹？"},
        {"icon": "✨", "t": "至亮至暗", "q": "最让你感到荣耀的时刻，以及那个让你至今不敢直视的绝望瞬间？"},
        {"icon": "⚡", "t": "身体警报", "q": "当你压力过载，身体哪个部位会先代替你发出尖叫？"},
        {"icon": "🤝", "t": "重要他人", "q": "谁是你生命中爱恨交织、影响至深的“关键他人”？"},
        {"icon": "🌀", "t": "命运迷宫", "q": "哪个瞬间是你发誓不再执行、却一直在重复上演的执念？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f"<p style='text-align:center; font-family:Cinzel;'>ROOM 0{st.session_state.step + 1}</p>", unsafe_allow_html=True)
        st.markdown(f'''<div class="film-frame"><div class="inner-box"><div style="font-size:3rem; margin-bottom:15px;">{r["icon"]}</div><h3 style="font-family:ZCOOL XiaoWei;">{r["t"]}</h3><p>{r["q"]}</p></div></div>''', unsafe_allow_html=True)
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=130, label_visibility="collapsed")
        if st.button("PROCEED / 前进"):
            if ans: st.session_state.answers.append(ans); st.session_state.step += 1; st.rerun()
    else:
        if st.button("DECODE ARCHIVE / 开启档案"):
            with st.spinner(""):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = (
                    f"Role: 心理考古师/专业咨询师\n要求：冷峻、深邃、语气温柔。每个模块限一句话。给出极具实操性的建议。\n数据：{' '.join(st.session_state.answers)}\n"
                    f"格式：\n### 📜 核心剧本\n(精准定性)\n\n### 🕯️ 觉察时刻\n(灵魂反思)\n\n### 🍃 行动指令\n(专业且温柔的建议)"
                )
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="memo-card">{res.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        if st.button("EXIT / 离开城堡"): reset()
