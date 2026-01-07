import streamlit as st
from openai import OpenAI

# 1. 视觉配置：极简高定 + 3D城堡甜点
st.set_page_config(page_title="The Dessert Castle", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    .stApp {
        background: #1a1a1a;
        background-image: 
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #d4a76c;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    .castle-room {
        background: #fdfdfd;
        color: #2c2c2c;
        border: 2px solid #2c2c2c;
        outline: 10px solid #fdfdfd;
        outline-offset: -15px;
        padding: 60px 40px;
        margin-top: 50px;
        box-shadow: 0 20px 0px #8c7355, 0 50px 100px rgba(0,0,0,0.5);
        position: relative;
        text-align: center;
    }

    .room-number {
        font-family: 'UnifrakturMaguntia', cursive;
        font-size: 2rem;
        color: #8c7355;
        position: absolute;
        top: 15px; left: 20px;
        opacity: 0.3;
    }

    .dessert-icon {
        font-size: 4rem;
        margin-bottom: 10px;
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.1));
        animation: floatCake 3s ease-in-out infinite;
    }
    @keyframes floatCake {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .room-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.2rem;
        letter-spacing: 4px;
        color: #4A3A3A;
    }

    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #ddd !important;
        color: #2c2c2c !important;
        font-size: 1.1rem !important;
        text-align: center !important;
    }

    .stButton > button {
        background-color: #8c7355 !important;
        color: #fdfdfd !important;
        border: none !important;
        letter-spacing: 5px;
        font-family: 'Cinzel', serif !important;
        width: 100%;
        margin-top: 20px;
    }

    .parchment-card {
        background: #fdf9e0;
        padding: 40px;
        border: 2px solid #a68e6b;
        color: #2c2c2c;
        box-shadow: 0 0 30px rgba(166, 142, 107, 0.3);
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态重置与循环逻辑
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

rooms = [
    {"icon": "🍰", "id": "I", "title": "原生底色", "q": "在这座城堡的地基下，哪一块甜点的味道最能唤醒你的最初记忆？"},
    {"icon": "✨", "id": "II", "title": "闪光时刻", "q": "当你站在最高塔尖，哪一次闪耀让你觉得自己像金箔点缀的蛋糕？"},
    {"icon": "🌑", "id": "III", "title": "至暗瞬间", "q": "在城堡最深的密室里，曾藏着你什么样的苦涩记忆？"},
    {"icon": "🌡️", "id": "IV", "title": "身体警报", "q": "如果你的身体是城堡的钟楼，压力下哪扇窗户最先震颤？"},
    {"icon": "🤝", "id": "V", "title": "重要他人", "q": "在城堡的盛宴上，谁像那道让你又爱又恨的招牌甜点？"},
    {"icon": "🌀", "id": "VI", "title": "循环怪圈", "q": "城堡里有没有哪条走廊，是你反复绕行却无法走出的甜点迷宫？"}
]

# 3. 页面渲染逻辑
if st.session_state.step < len(rooms):
    r = rooms[st.session_state.step]
    
    st.markdown(f'''
        <div class="castle-room">
            <div class="room-number">{r['id']}</div>
            <div class="dessert-icon">{r['icon']}</div>
            <div class="room-title">{r['title']}</div>
            <h4 style="font-weight:300;">{r['q']}</h4>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"input_{st.session_state.step}", height=120, label_visibility="collapsed")
    
    if st.button("推开下一扇门"):
        if ans:
            st.session_state.answers.append(ans)
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("请留下这段墙砖上的文字...")

else:
    st.markdown('<h2 style="text-align:center;">城堡叙事已完成封存</h2>', unsafe_allow_html=True)
    
    if st.button("解密我的甜点档案"):
        with st.spinner("正在注塑、重构叙事中..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\\n".join(st.session_state.answers)
                
                prompt = f"你是一个名为MindMemo的心理考古引擎。对以下内容进行冷峻深刻的分析，不要客套话。内容：{full_context}。格式：### 🏷️ 灵魂标签 \\n ### 🧠 脚本监测 (CBT) \\n ### 🍃 进化路径 (ACT)"
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''<div class="parchment-card">{response.choices[0].message.content}</div>''', unsafe_allow_html=True)
                
            except Exception as e:
                st.error("余额不足或连接失败，请检查DeepSeek账户。")

    # 循环逻辑按钮：回到开头
    if st.button("走出城堡，重新开启旅程"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()
