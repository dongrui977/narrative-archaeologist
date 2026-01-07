import streamlit as st
from openai import OpenAI

# 1. 视觉配置：韦斯安德森对称美学 + 3D 景深层次
st.set_page_config(page_title="The Soul Palace", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 城堡全景：质感复古背景 */
    .stApp {
        background: #E6E1D6;
        background-image: linear-gradient(rgba(230,225,214,0.8), rgba(230,225,214,0.8)),
            url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        color: #423629;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 首页入口 */
    .portal-door {
        background: #FDFCF0;
        border: 2px solid #423629;
        padding: 50px 30px;
        text-align: center;
        box-shadow: 15px 15px 0px #423629;
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .portal-door:hover {
        transform: translateY(-10px) rotateY(-5deg);
        box-shadow: 20px 20px 0px #D4A373;
        border-color: #D4A373;
    }

    /* 胶片感容器 */
    .film-frame {
        background: #1A1A1A;
        padding: 40px 20px;
        border-radius: 4px;
        position: relative;
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    }
    .film-frame::before, .film-frame::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: #E6E1D6; font-size: 8px; letter-spacing: 15px;
        position: absolute; width: 100%; text-align: center; left: 0;
    }
    .film-frame::before { top: 10px; }
    .film-frame::after { bottom: 10px; }

    .inner-content {
        background: #FDFCF0;
        padding: 40px;
        border: 1px solid #D4A373;
        text-align: center;
    }

    /* 按钮：火漆印感 */
    .stButton > button {
        background-color: #423629 !important;
        color: #FDFCF0 !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 12px 0 !important;
        width: 100%;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 5px;
        transition: 0.3s;
        box-shadow: 4px 4px 0px #D4A373;
    }
    .stButton > button:hover {
        background-color: #D4A373 !important;
        color: #1A1A1A !important;
    }
    
    /* 结果卡片 */
    .result-card {
        background: white;
        padding: 50px;
        border: 1px solid #D4A373;
        box-shadow: 0 0 50px rgba(212, 163, 115, 0.3);
        text-align: left;
        line-height: 1.8;
    }
    .result-card h3 {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem !important; /* 强制统一字号 */
        font-weight: 600 !important;
        color: #423629 !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        border-bottom: 1px solid #EEE;
        padding-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态逻辑
if 'mode' not in st.session_state: st.session_state.mode = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = []

def reset_to_hall():
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
        st.markdown('<div class="portal-door"><div style="font-size:3rem; margin-bottom:20px;">🍮</div><h3 style="font-family:Cinzel;">DAILY RELIEF</h3><p style="font-size:0.8rem; opacity:0.7;">日常情绪清理<br>MindMemo 引擎</p></div>', unsafe_allow_html=True)
        if st.button("进入日常门扉"):
            st.session_state.mode = 'daily'
            st.rerun()

    with col2:
        st.markdown('<div class="portal-door"><div style="font-size:3rem; margin-bottom:20px;">🏰</div><h3 style="font-family:Cinzel;">DEEP ARCHIVE</h3><p style="font-size:0.8rem; opacity:0.7;">深度生命考古<br>叙事重构师</p></div>', unsafe_allow_html=True)
        if st.button("推开档案暗室"):
            st.session_state.mode = 'deep'
            st.rerun()

# --- 第二幕：日常处理模式 ---
elif st.session_state.mode == 'daily':
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>MINDMEMO ENGINE</h2>", unsafe_allow_html=True)
    st.markdown('<div class="film-frame"><div class="inner-content"><h4>现在，请倾倒出您此刻堆积的情绪碎片。</h4></div></div>', unsafe_allow_html=True)
    
    daily_input = st.text_area("", height=200, label_visibility="collapsed", placeholder="引擎正静默等待您的输入...")
    
    if st.button("执行静默分析"):
        if daily_input:
            with st.spinner("剥离噪音中..."):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                # 修复了标题对齐和简洁度
                prompt = (
                    f"Role: MindMemo引擎\n"
                    f"要求：专业的心理咨询师，产出口语化有疗愈感。\n"
                    f"内容：{daily_input}\n"
                    f"格式：\n"
                    f"### 🏷️ 智能标签\n(3个关键词)\n\n"
                    f"### 🧠 思维侦探 (CBT)\n(简短洞察)\n\n"
                    f"### 🍃 接纳与行动 (ACT)\n(一句话建议)"
                )
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="result-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
    
    if st.button("走出大门，返回城堡入口 🔄"):
        reset_to_hall()

# --- 第三幕：深度考古模式 ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "title": "原生底色", "q": "原生底色：出生在哪里？童年记忆中最深刻的一个画面是什么？"},
        {"icon": "✨", "title": "高光至暗", "q": "高光与至暗：哪一刻让你觉得自己是世界的中心？哪一刻感到彻底绝望？"},
        {"icon": "💊", "title": "身体记号", "q": "身体记号：你的身体生过什么病？压力大时哪里先报警？"},
        {"icon": "🤝", "title": "重要他人", "q": "关键关系人：谁是你生命中爱恨交织的“重要他人”？"},
        {"icon": "🔀", "title": "转折执念", "q": "转折与执念：你发誓不想重复却一直在重复的模式是什么？"}
    ]

    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f"<h3 style='text-align:center; font-family:Cinzel;'>ROOM {st.session_state.step + 1}</h3>", unsafe_allow_html=True)
        st.markdown(f'''<div class="film-frame"><div class="inner-content"><div style="font-size:3rem;">{r['icon']}</div><h3 style="font-family:ZCOOL XiaoWei;">{r['title']}</h3><p>{r['q']}</p></div></div>''', unsafe_allow_html=True)
        
        ans = st.text_area("", key=f"d_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="请详细刻录...")
        if st.button("推开下一扇门"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
    else:
        st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>THE FINAL ARCHIVE</h2>", unsafe_allow_html=True)
        if st.button("生成叙事重构报告"):
            with st.spinner("考古学家正在修复您的生命剧本..."):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_data = "\n".join(st.session_state.answers)
                # 修复了报告的简洁度
                prompt = (
                    f"Role: 心理考古师\n"
                    f"要求：专业的心理咨询师，产出口语化有疗愈感。\n"
                    f"内容：{full_data}\n"
                    f"格式：\n"
                    f"### 📜 叙事重构\n(精简一句话)\n\n"
                    f"### 🎯 核心图式\n(精简一句话)\n\n"
                    f"### ⚡ 躯体标记\n(精简一句话)\n\n"
                    f"### ⚓ 未完情结\n(精简一句话)\n\n"
                    f"### 🕯️ 觉察时刻\n(精简一句话反思)"
                )
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="result-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        if st.button("结束考古，返回城堡入口 🔄"):
            reset_to_hall()
