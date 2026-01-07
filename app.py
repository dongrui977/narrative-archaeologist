import streamlit as st
from openai import OpenAI

# 1. 城堡建筑美学：哥特式质感、复古小蛋糕、3D 层次
st.set_page_config(page_title="The Narrative Castle", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：深邃城堡石纹感 */
    .stApp {
        background: #1a1a1a;
        background-image: 
            linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
            url("https://www.transparenttextures.com/patterns/dark-leather.png");
        color: #d4a76c;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 城堡房间（主容器）：3D 浮雕与阴影 */
    .castle-room {
        background: #fdfdfd;
        color: #2c2c2c;
        border: 2px solid #2c2c2c;
        outline: 10px solid #fdfdfd;
        outline-offset: -15px;
        padding: 80px 60px;
        margin-top: 50px;
        box-shadow: 
            0 20px 0px #8c7355, /* 模拟建筑底座 */
            0 50px 100px rgba(0,0,0,0.5);
        position: relative;
        animation: roomEntrance 1.5s ease-out;
    }

    @keyframes roomEntrance {
        from { transform: scale(0.9) translateY(50px); opacity: 0; }
        to { transform: scale(1) translateY(0); opacity: 1; }
    }

    /* 哥特式房间编号 */
    .room-number {
        font-family: 'UnifrakturMaguntia', cursive;
        font-size: 2.5rem;
        color: #8c7355;
        position: absolute;
        top: 20px;
        left: 30px;
        opacity: 0.2;
    }

    .castle-label {
        font-family: 'Cinzel', serif;
        font-size: 0.8rem;
        letter-spacing: 6px;
        margin-bottom: 20px;
        display: block;
        color: #8c7355;
    }

    .room-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.2rem;
        margin-bottom: 40px;
        letter-spacing: 4px;
    }

    /* 输入区域：像在城堡古籍上书写 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #ddd !important;
        color: #2c2c2c !important;
        font-size: 1.2rem !important;
        text-align: center !important;
        border-radius: 0 !important;
        padding: 20px !important;
    }
    .stTextArea textarea:focus {
        border-bottom: 2px solid #8c7355 !important;
        box-shadow: none !important;
    }

    /* 按钮：沉重的青铜门栓感 */
    .stButton > button {
        background-color: #2c2c2c !important;
        color: #fdfdfd !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 15px 50px !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 5px;
        font-size: 0.9rem !important;
        box-shadow: 5px 5px 0px #8c7355;
        transition: 0.2s;
        margin-top: 40px;
    }
    .stButton > button:active {
        transform: translate(3px, 3px);
        box-shadow: 2px 2px 0px #8c7355;
    }

    /* 圣光闪烁：城堡密室里的宝藏卡片 */
    .treasure-card {
        background: white;
        padding: 50px;
        border: 2px solid #2c2c2c;
        position: relative;
        animation: castleGlow 4s infinite alternate;
        text-align: left;
        line-height: 2;
    }
    @keyframes castleGlow {
        from { box-shadow: 0 0 20px rgba(140, 115, 85, 0.1); }
        to { box-shadow: 0 0 60px rgba(140, 115, 85, 0.4), inset 0 0 30px rgba(140, 115, 85, 0.05); }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态逻辑：城堡房间管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 定义 6 个具有叙事深度的房间
rooms = [
    {"icon": "🥧", "id": "I", "label": "THE ORIGIN", "title": "原生底色", "q": "在这座城堡的地基下，哪一张童年画面被埋藏得最深？"},
    {"icon": "✨", "id": "II", "label": "THE RADIANCE", "title": "闪光时刻", "q": "当你站在城堡顶端，那一刻你觉得自己比星辰还耀眼？"},
    {"icon": "🌑", "id": "III", "label": "THE ABYSS", "title": "至暗瞬间", "q": "在城堡最冷的密室里，曾藏着你什么样的无助？"},
    {"icon": "⚡", "id": "IV", "label": "THE ECHO", "title": "身体警报", "q": "如果你的身体是一座建筑，哪扇窗户在压力下最先震颤？"},
    {"icon": "🤝", "id": "V", "label": "THE PORTRAIT", "title": "重要他人", "q": "城堡墙上挂着的那个肖像，他给你的感觉是甜美还是辛辣？"},
    {"icon": "🌀", "title": "循环怪圈", "id": "VI", "label": "THE LABYRINTH", "q": "城堡里有没有哪条走廊，是你反复绕行却无法走出的？"}
]

# 3. 城堡流程渲染
if st.session_state.step < len(rooms):
    r = rooms[st.session_state.step]
    
    st.markdown(f'''
        <div class="castle-room">
            <div class="room-number">{r['id']}</div>
            <div class="castle-label">{r['label']}</div>
            <div style="font-size: 4rem; margin-bottom: 20px;">{r['icon']}</div>
            <div class="room-title">{r['title']}</div>
            <h4 style="font-weight: 300;">{r['q']}</h4>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"r_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="请刻录下这段墙砖上的文字...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("推开下一扇门"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="room-title" style="text-align:center; margin-top:100px; color:#d4a76c;">ARCHIVE COMPLETE</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("解密我的灵魂档案"):
            with st.spinner("城堡密室正在开启..."):
                try:
                    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                    full_context = "\n".join(st.session_state.answers)
                    
                    prompt = f"""
                    你是一个名为 "MindMemo" 的心理考古引擎。
                    任务：对用户的城堡叙事进行静默分析，生成极其简短、冷峻且深刻的“灵魂卡片”。
                    分析视角：ACT + CBT。
                    输入：{full_context}
                    格式：
                    ### 🏷️ 灵魂标签
                    ### 🧠 脚本监测 (CBT)
                    ### 🍃 进化路径 (ACT)
                    """
                    
                    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                    
                    st.markdown(f'''
                        <div class="treasure-card">
                            <div style="text-align:center; font-family:Cinzel; letter-spacing:5px; color:#8c7355; margin-bottom:30px;">MINDMEMO DOSSIER</div>
                            {response.choices[0].message.content}
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    if st.button("走出城堡重新开启之旅"):
                        st.session_state.step = 0
                        st.session_state.answers = []
                        st.rerun()
                        
                except Exception as e:
                    st.error("API Error.")
