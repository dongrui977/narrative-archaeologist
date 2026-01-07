import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：哥特城堡 + 复古甜点 + 复杂层次
st.set_page_config(page_title="The Dessert Castle Archives", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Cinzel:wght@400;700&family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@200;500&display=swap');

    /* 全局背景：深邃城堡石纹 + 隐约甜点浮雕 */
    .stApp {
        background: #1e1e1e;
        background-image: 
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url("https://www.transparenttextures.com/patterns/dark-leather.png"),
            url("https://img.icons8.com/color/96/000000/cupcake.png"), /* 隐约的背景甜点 */
            url("https://img.icons8.com/color/96/000000/macaron.png");
        background-repeat: repeat, repeat, repeat, repeat;
        background-position: 0 0, 0 0, 100px 100px, 250px 250px;
        background-size: auto, auto, 120px 120px, 100px 100px;
        background-attachment: fixed;
        color: #d4a76c;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 城堡房间（主容器）：3D 浮雕与阴影，保持建筑感 */
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
        border-radius: 4px; /* 微妙的圆角，调和城堡与甜点 */
    }

    @keyframes roomEntrance {
        from { transform: scale(0.9) translateY(50px); opacity: 0; }
        to { transform: scale(1) translateY(0); opacity: 1; }
    }

    /* 哥特式房间编号与标题 */
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
        color: #4A3A3A; /* 更深的颜色，配合甜点 */
    }

    /* 甜点图标：3D 悬浮感 */
    .dessert-icon {
        font-size: 4rem;
        margin-bottom: 25px;
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.2));
        animation: floatCake 3s ease-in-out infinite;
    }
    @keyframes floatCake {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(-3deg); }
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

    /* 按钮：青铜门栓 + 甜点黄油色 */
    .stButton > button {
        background-color: #8c7355 !important; /* 甜点黄油棕 */
        color: #fdfdfd !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 15px 50px !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 5px;
        font-size: 0.9rem !important;
        box-shadow: 5px 5px 0px #d4a76c; /* 甜点金色阴影 */
        transition: 0.2s;
        margin-top: 40px;
    }
    .stButton > button:active {
        transform: translate(3px, 3px);
        box-shadow: 2px 2px 0px #d4a76c;
    }

    /* 圣光闪烁：城堡密室里的宝藏卡片 (羊皮纸质感) */
    .parchment-card {
        background: #fdf9e0; /* 羊皮纸色 */
        padding: 50px;
        border: 2px solid #a68e6b; /* 古旧边框色 */
        position: relative;
        animation: treasureGlow 4s infinite alternate;
        text-align: left;
        line-height: 2;
        box-shadow: 0 0 30px rgba(140, 115, 85, 0.2);
    }
    @keyframes treasureGlow {
        from { box-shadow: 0 0 20px rgba(166, 142, 107, 0.1); }
        to { box-shadow: 0 0 50px rgba(166, 142, 107, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.05); }
    }
    .parchment-card h3 {
        font-family: 'Cinzel', serif;
        font-size: 1rem;
        color: #8c7355;
        border-bottom: 1px dashed #a68e6b; /* 虚线分隔 */
        padding-bottom: 10px;
        margin-top: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 状态逻辑：城堡房间管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 定义 6 个具有叙事深度的城堡房间，每个房间有专属甜点图标
rooms = [
    {"icon": "🍰", "id": "I", "label": "THE FOUNDATION", "title": "原生底色", "q": "在这座城堡的地基下，哪一块甜点的味道最能唤醒你的最初记忆？"},
    {"icon": "✨", "id": "II", "label": "THE CROWN", "title": "闪光时刻", "q": "当你站在城堡最高塔尖，哪一次闪耀让你觉得自己像金箔点缀的蛋糕？"},
    {"icon": "☕", "id": "III", "label": "THE DUNGEON", "title": "至暗瞬间", "q": "在城堡最深的酒窖里，曾藏着你什么样的苦涩如浓咖啡般的记忆？"},
    {"icon": "🔔", "id": "IV", "label": "THE ECHOING BELL", "title": "身体警报", "q": "如果你的身体是城堡的钟楼，哪一声钟鸣在压力下最先敲响？"},
    {"icon": "🥂", "id": "V", "label": "THE GRAND FEAST", "title": "重要他人", "q": "在城堡的盛宴上，谁像那道让你又爱又恨的招牌甜点？"},
    {"icon": "🌀", "id": "VI", "label": "THE LABYRINTH", "title": "循环怪圈", "q": "城堡里有没有哪条弯曲的走廊，是你反复绕行却无法走出的甜点迷宫？"}
]

# 3. 城堡流程渲染
if st.session_state.step < len(rooms):
    r = rooms[st.session_state.step]
    
    st.markdown(f'''
        <div class="castle-room">
            <div class="room-number">{r['id']}</div>
            <div class="castle-label">{r['label']}</div>
            <div class="dessert-icon">{r['icon']}</div> {/* 甜点图标 */}
            <div class="room-title">{r['title']}</div>
            <h4 style="font-weight: 300;">{r['q']}</h4>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"r_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="请将您的记忆刻录在古老的墙壁上...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("推开下一扇门"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="room-title" style="text-align:center; margin-top:100px; color:#d4a76c;">城堡叙事已完成封存</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("解密我的甜点档案"):
            with st.spinner("城堡密室正在开启，古老食谱即将揭示..."):
                try:
                    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                    full_context = "\n".join(st.session_state.answers)
                    
                    prompt = f"""
                    你是一个名为 "MindMemo" 的心理考古引擎。
                    任务：对用户的城堡叙事进行静默分析，生成极其简短、冷峻且深刻的“灵魂甜点卡片”。
                    分析视角：ACT + CBT。不要建议，只要揭露。
                    输入：{full_context}
                    格式：
                    ### 🏷️ 灵魂标签
                    ### 🧠 脚本监测 (CBT)
                    ### 🍃 进化路径 (ACT)
                    """
                    
                    response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                    
                    st.markdown(f'''
                        <div class="parchment-card">
                            <div style="text-align:center; font-family:Cinzel; letter-spacing:5px; color:#8c7355; margin-bottom:30px;">THE SECRET RECIPE</div>
                            {response.choices[0].message.content}
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # 关键的循环逻辑：回到最初的第一个问题
                    if st.button("走出城堡，重新开启旅程"):
                        st.session_page.step = 0
                        st.session_state.answers = []
                        st.rerun()
                        
                except Exception as e:
                    st.error("API Error: 城堡的魔法失效了。")
